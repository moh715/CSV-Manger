from project import CsvManger, marge, delete_file, classify, add_to_file, delete_from_file
import pytest
import os

def test_marge():
    assert marge([2,4,5], [1,3,6]) == [1,2,3,4,5,6]
    assert marge([12, 13], []) == [12, 13]
    assert marge([{"one":12}], [{"one":5}], lambda s: s["one"]) == [{"one":5}, {"one":12}]

def test_delete_file(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    g = CsvManger.make_file("test", ["one", "two"])
    r = delete_file("test")
    assert r == "File 'test' has been deleted."


def test_classify():
    classify_tests = {"hello": ("greeting", None),
                      "bye":("farewell", None),
                      "jienaie": ("fallback", None),
                      "open test file":("open_file", "test"),
                      "delete test file":("delete_file", "test"),
                      "make test file": ("make_file", "test"),
                      "add to test list": ("add_to_file", "test"),
                      "add 'moh, ho,13' to test list" : ("add_to_file", ["test", "'moh, ho,13'"])
                      }
    for test, value in classify_tests.items():
        assert classify(test) == value


@pytest.mark.parametrize(
    "mock_inputs, expected_output",
    [
        (["Alice", "25", "New York"], "Success! 1 new entries have been added to 'test'."),
        (["Bob, jo", "30, 14", "Los Angeles, New York"], "Success! 2 new entries have been added to 'test'."),
        (["Charlie, jo", "40", "Chicago"], "Error: All fields must have the same number of values. Please enter the same number of values for each field.(use '.' for empty values)"),
    ],
)


def test_add_to_file(monkeypatch, mock_inputs, expected_output):
    f = CsvManger.make_file("test", ["name", "work", "city"])
    inputs = iter(mock_inputs)  # Create an iterator for user inputs
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = add_to_file("test")
    assert result == expected_output

def test_delete_from_file():
    f = CsvManger("test")
    data_after = []
    for i in range(12):
        add_to_file("test",f"test,{i},{i**2}")
        if i <= 2:
            data_after.append({"name":"test", "work": str(i), "city":str(i**2)})
    delete_from_file("test","work > 2")
    assert sorted(f.data(),key=lambda x: x["work"])== data_after
    delete_from_file("test", "work = 0")
    assert sorted(f.data(),key=lambda x: x["work"]) == data_after[1:]
