import os
from datetime import datetime, timezone

import pytest
from mod_ngarn.api import add_job
from mod_ngarn.connection import get_connection
from mod_ngarn.utils import create_table


@pytest.mark.asyncio
async def test_add_job_should_return_inserted_record():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    job_id = "job-1"
    fn_name = "fn_name"
    args = ["a", "b"]
    kwargs = {"a": "1", "b": "2"}
    res = await add_job(cnx, "modngarn_job", job_id, fn_name, kwargs=kwargs, args=args)

    assert res["id"] == job_id
    assert res["fn_name"] == fn_name
    assert res["args"] == args
    assert res["kwargs"] == kwargs
    assert res["priority"] == 0

    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


@pytest.mark.asyncio
async def test_add_job_with_only_fn_name_should_store_empty_args_and_kwargs():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    job_id = "job-1"
    fn_name = "fn_name"
    await add_job(cnx, "modngarn_job", job_id, fn_name)

    res = await cnx.fetchrow(
        f"SELECT id, fn_name, args, kwargs, priority FROM {queue_table}"
    )

    assert res["id"] == job_id
    assert res["fn_name"] == fn_name
    assert res["args"] == []
    assert res["kwargs"] == {}
    assert res["priority"] == 0

    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


@pytest.mark.asyncio
async def test_add_job_should_store_all_of_parameter_as_input():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    job_id = "job-1"
    fn_name = "fn_name"
    args = ["a", "b"]
    kwargs = {"a": "1", "b": "2"}
    priority = 3
    schedule_time = datetime(2018, 1, 2, 0, 0, tzinfo=timezone.utc)

    await add_job(
        cnx,
        queue_table,
        job_id,
        fn_name,
        priority=priority,
        args=args,
        kwargs=kwargs,
        schedule_time=schedule_time,
    )

    res = await cnx.fetchrow(
        f"SELECT id, fn_name, args, kwargs, priority, scheduled FROM {queue_table}"
    )

    assert res["id"] == job_id
    assert res["fn_name"] == fn_name
    assert res["args"] == args
    assert res["kwargs"] == kwargs
    assert res["priority"] == priority
    assert res["scheduled"] == schedule_time

    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()


async def async_sum(first, second):
    return first + second


@pytest.mark.asyncio
async def test_add_job_should_convert_callable_to_string_function_name():
    queue_table = "public.modngarn_job"
    await create_table("public", "modngarn_job")
    cnx = await get_connection()
    job_id = "job-1"
    fn_name = async_sum
    await add_job(cnx, "modngarn_job", job_id, fn_name)

    res = await cnx.fetchrow(
        f"SELECT id, fn_name, args, kwargs, priority FROM {queue_table}"
    )

    assert res["id"] == job_id
    assert res["fn_name"] == "tests.test_api.async_sum"
    assert res["args"] == []
    assert res["kwargs"] == {}
    assert res["priority"] == 0

    await cnx.execute(f"TRUNCATE TABLE {queue_table};")
    await cnx.close()
