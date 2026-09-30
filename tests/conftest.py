def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Adds a custom AI MODEL TEST SUMMARY at the end of the test run."""
    stats = terminalreporter.stats
    
    passed = len(stats.get('passed', []))
    failed = len(stats.get('failed', []))
    
    all_reports = stats.get('passed', []) + stats.get('failed', [])
    
    func = len([x for x in all_reports if 'test_chatbot' in x.nodeid])
    neg = len([x for x in all_reports if 'test_negative_cases' in x.nodeid and 'test_negative' in x.nodeid])
    bound = len([x for x in all_reports if 'test_boundary' in x.nodeid])
    cons = len([x for x in all_reports if 'test_consistency' in x.nodeid])
    reg = len([x for x in all_reports if 'test_regression' in x.nodeid])
    pi = len([x for x in all_reports if 'test_prompt_injection' in x.nodeid])
    api = len([x for x in all_reports if 'test_api_failures' in x.nodeid])
    
    infra_errors = api
    for f in stats.get('failed', []):
        if hasattr(f, 'longreprtext') and 'API/INFRASTRUCTURE FAILURE' in f.longreprtext:
            infra_errors += 1

    terminalreporter.write_sep("=", "AI MODEL TEST SUMMARY")
    terminalreporter.write_line(f"Functional Tests:       {func}")
    terminalreporter.write_line(f"Negative Tests:         {neg}")
    terminalreporter.write_line(f"Boundary Tests:         {bound}")
    terminalreporter.write_line(f"Consistency Tests:      {cons}")
    terminalreporter.write_line(f"Regression Tests:       {reg}")
    terminalreporter.write_line(f"Prompt Injection:       {pi}")
    terminalreporter.write_line("")
    terminalreporter.write_line(f"Passed:                 {passed}")
    terminalreporter.write_line(f"Failed:                 {failed}")
    terminalreporter.write_line(f"Infrastructure Errors:  {infra_errors}")
