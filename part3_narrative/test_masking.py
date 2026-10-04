from masking import alias_for, assert_no_raw_names_leak


def test_masking():
    assert alias_for("RS019") == "ALIAS-19"
    names = ["Mumbai Reseller 1", "Mumbai Reseller 4"]
    safe = "West - ALIAS-19 should be reviewed."
    unsafe = "West - Mumbai Reseller 1 should be reviewed."
    assert assert_no_raw_names_leak(safe, names) is True
    assert assert_no_raw_names_leak(unsafe, names) is False


if __name__ == "__main__":
    test_masking()
    print("PASS test_masking")
