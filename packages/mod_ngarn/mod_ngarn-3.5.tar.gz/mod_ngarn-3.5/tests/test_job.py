import os
from datetime import datetime
from unittest import TestCase
import asyncio

import freezegun
import pytest
from mod_ngarn.connection import get_connection
from mod_ngarn.utils import create_table
from mod_ngarn.worker import Job, JobRunner
from decimal import Decimal


def sync_dummy_job(text):
    return text


async def async_dummy_job(text):
    return text


def raise_dummy_job():
    raise KeyError()


@pytest.mark.asyncio
async def test_job_execute_builtin_success():
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    job = Job(cnx, "public", "modngarn_job", "job-1", "sum", 1, [[1, 2]], {})
    result = await job.execute()
    assert result == 3
    await cnx.close()


@pytest.mark.asyncio
async def test_job_execute_sync_fn_success():
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    job = Job(
        cnx,
        "public",
        "modngarn_job",
        "job-1",
        "tests.test_job.sync_dummy_job",
        1,
        ["hello"],
        {},
    )
    result = await job.execute()
    assert result == "hello"
    await cnx.close()


@pytest.mark.asyncio
async def test_job_execute_async_fn_success():
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    job = Job(
        cnx,
        "public",
        "modngarn_job",
        "job-1",
        "tests.test_job.async_dummy_job",
        1,
        ["hello"],
        {},
    )
    result = await job.execute()
    assert result == "hello"
    await cnx.close()


@pytest.mark.asyncio
async def test_job_success_record_to_db():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.execute(
        """
    INSERT INTO {queue_table} (id, fn_name, args) VALUES ('job-1', 'tests.test_job.async_dummy_job', '["hello"]')
    """.format(
            queue_table=queue_table
        )
    )
    job = Job(
        cnx,
        "public",
        "modngarn_job",
        "job-1",
        "tests.test_job.async_dummy_job",
        0,
        ["hello"],
        {},
    )
    result = await job.execute()
    assert result == "hello"
    job = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-1")
    assert job["result"] == "hello"
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


@pytest.mark.asyncio
async def test_job_failed_record_to_db():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.execute(
        """
    INSERT INTO {queue_table} (id, fn_name, args) VALUES ('job-2', 'tests.test_job.raise_dummy_job', '["hello"]')
    """.format(
            queue_table=queue_table
        )
    )
    job = Job(
        cnx, "public", "modngarn_job", "job-2", "tests.test_job.raise_dummy_job", 0
    )
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["result"] == None
    assert job_db["priority"] == 1
    assert "KeyError" in job_db["reason"]
    assert "Traceback" in job_db["reason"]

    log_db = await cnx.fetchval(
        f"SELECT COUNT(*) FROM {queue_table}_error WHERE id=$1", "job-2"
    )
    assert log_db == 1

    job = Job(
        cnx, "public", "modngarn_job", "job-2", "tests.test_job.raise_dummy_job", 1
    )
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["result"] == None
    assert job_db["priority"] == 2
    assert "KeyError" in job_db["reason"]
    assert "Traceback" in job_db["reason"]

    log_db = await cnx.fetchval(
        f"SELECT COUNT(*) FROM {queue_table}_error WHERE id=$1", "job-2"
    )
    assert log_db == 2

    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


@freezegun.freeze_time("2018-01-01T12:00:00+00:00")
@pytest.mark.asyncio
async def test_job_failed_exponential_delay_job_based_on_priority():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.execute(
        """
    INSERT INTO {queue_table} (id, fn_name, args) VALUES ('job-2', 'tests.test_job.raise_dummy_job', '["hello"]')
    """.format(
            queue_table=queue_table
        )
    )
    job = Job(
        cnx, "public", "modngarn_job", "job-2", "tests.test_job.raise_dummy_job", 0
    )
    # First failed, should delay 1 sec
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["priority"] == 1
    assert job_db["scheduled"].isoformat() == "2018-01-01T12:00:01+00:00"

    # Second failed, should delay e^2 sec
    job.priority = job_db["priority"]
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["priority"] == 2
    assert job_db["scheduled"].isoformat() == "2018-01-01T12:00:02.718282+00:00"

    # Third failed, should delay e^3 sec
    job.priority = job_db["priority"]
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["priority"] == 3
    assert job_db["scheduled"].isoformat() == "2018-01-01T12:00:07.389056+00:00"

    # 10th failed, should delay e^10 sec
    job.priority = 10
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["scheduled"].isoformat() == "2018-01-01T18:07:06.465795+00:00"

    # 21th failed, should be priority 21
    job.priority = 21
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["scheduled"].isoformat() == "2059-10-17T13:42:14.483215+00:00"

    # 22th failed, should be priority 21
    job.priority = 22
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["scheduled"].isoformat() == "2059-10-17T13:42:14.483215+00:00"

    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


@freezegun.freeze_time("2018-01-01T12:00:00+00:00")
@pytest.mark.asyncio
async def test_job_failed_can_set_max_delay():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.execute(
        """
    INSERT INTO {queue_table} (id, fn_name, args) VALUES ('job-2', 'tests.test_job.raise_dummy_job', '["hello"]')
    """.format(
            queue_table=queue_table
        )
    )
    job = Job(
        cnx,
        "public",
        "modngarn_job",
        "job-2",
        "tests.test_job.raise_dummy_job",
        0,
        max_delay=1.5,
    )
    # First failed, should delay 1 sec
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["priority"] == 1
    assert job_db["scheduled"].isoformat() == "2018-01-01T12:00:01+00:00"

    # Second failed, should delay 1.5 sec
    job.priority = job_db["priority"]
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["priority"] == 2
    assert job_db["scheduled"].isoformat() == "2018-01-01T12:00:01.500000+00:00"

    # Third failed, should delay 1.5 sec
    job.priority = job_db["priority"]
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["priority"] == 3
    assert job_db["scheduled"].isoformat() == "2018-01-01T12:00:01.500000+00:00"

    # 10th failed, should delay 1.5 sec
    job.priority = 10
    await job.execute()
    job_db = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-2")
    assert job_db["scheduled"].isoformat() == "2018-01-01T12:00:01.500000+00:00"

    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


@pytest.mark.asyncio
async def test_job_runner_success_process():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.execute(
        """
    INSERT INTO {queue_table} (id, fn_name, args) VALUES ('job-1', 'tests.test_job.async_dummy_job', '["hello"]')
    """.format(
            queue_table=queue_table
        )
    )
    job_runner = JobRunner()
    await job_runner.run("public", "modngarn_job", 1, None)
    job = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-1")
    assert job["result"] == "hello"
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


@pytest.mark.asyncio
async def test_job_runner_can_define_limit():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    await cnx.execute(f'TRUNCATE TABLE "modngarn_job";')
    await cnx.execute(
        """INSERT INTO "modngarn_job" (id, fn_name, args)
            SELECT 'job-' || s, 'tests.test_job.async_dummy_job', '["hello"]'
            FROM generate_series(0, 100) s;"""
    )
    job_runner = JobRunner()
    await job_runner.run("public", "modngarn_job", 10, None)
    total_processed = await cnx.fetchval(
        f'SELECT COUNT(*) FROM "modngarn_job" WHERE executed IS NOT NULL'
    )
    assert total_processed == 10
    await job_runner.run("public", "modngarn_job", 10, None)
    total_processed = await cnx.fetchval(
        f'SELECT COUNT(*) FROM "modngarn_job" WHERE executed IS NOT NULL'
    )
    assert total_processed == 20
    await cnx.execute(f'TRUNCATE TABLE "modngarn_job";')
    await cnx.close()


@pytest.mark.asyncio
async def test_job_notify_when_job_is_inserted():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    q = asyncio.Queue()

    def listener(cnx, pid: int, channel: str, payload: str):
        q.put_nowait(channel)

    await cnx.add_listener("public_modngarn_job", listener)
    await cnx.execute(
        """
    INSERT INTO {queue_table} (id, fn_name, args, reason) VALUES ('job-1', 'tests.test_job.async_dummy_job', '["hello"]', 'some error message')
    """.format(
            queue_table=queue_table
        )
    )
    assert q.get_nowait() == "public_modngarn_job"
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


@pytest.mark.asyncio
async def test_job_runner_success_should_clear_error_msg():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.execute(
        """
    INSERT INTO {queue_table} (id, fn_name, args, reason) VALUES ('job-1', 'tests.test_job.async_dummy_job', '["hello"]', 'some error message')
    """.format(
            queue_table=queue_table
        )
    )
    job_runner = JobRunner()
    await job_runner.run("public", "modngarn_job", 1, None)
    job = await cnx.fetchrow(f"SELECT * FROM {queue_table} WHERE id=$1", "job-1")
    assert job["result"] == "hello"
    assert job["reason"] is None
    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


class TestExitFromJobRunner(TestCase):
    def async_test(f):
        def wrapper(*args, **kwargs):
            coro = asyncio.coroutine(f)
            future = coro(*args, **kwargs)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(future)

        return wrapper
