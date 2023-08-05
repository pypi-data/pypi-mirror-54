import os
import platform
import sys
from timeit import default_timer

import click
from colorama import init

from ward.collect import get_info_for_modules, get_tests_in_modules, load_modules
from ward.fixtures import fixture_registry
from ward.suite import Suite
from ward.terminal import ExitCode, SimpleTestResultWrite
from ward.test_result import TestOutcome

init()

if platform.system() == "Windows":
    os.system('color')


@click.command()
@click.option(
    "-p", "--path", default=".", type=click.Path(exists=True), help="Path to tests."
)
@click.option(
    "-f", "--filter", help="Only run tests whose names contain the filter argument as a substring."
)
@click.option(
    "--fail-limit", type=int, help="The number of failures to cancel the run after."
)
def run(path, filter, fail_limit):
    start_run = default_timer()

    mod_infos = get_info_for_modules(path)
    modules = list(load_modules(mod_infos))
    tests = list(get_tests_in_modules(modules, filter=filter))
    time_to_collect = default_timer() - start_run

    suite = Suite(tests=tests, fixture_registry=fixture_registry)
    test_results = suite.generate_test_runs()

    writer = SimpleTestResultWrite(suite=suite)
    results = writer.output_all_test_results(
        test_results,
        time_to_collect=time_to_collect,
        fail_limit=fail_limit,
    )
    time_taken = default_timer() - start_run
    writer.output_test_result_summary(results, time_taken)

    if any(r.outcome == TestOutcome.FAIL for r in results):
        exit_code = ExitCode.TEST_FAILED
    else:
        exit_code = ExitCode.SUCCESS

    sys.exit(exit_code.value)
