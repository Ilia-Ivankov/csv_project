from csv_reader import csv_reader
import pytest
import csv


def test_csv_reader():
    data = csv_reader.csv_parser('tests/fixtures/products.csv')
    with open('tests/fixtures/products.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            assert all(item in data for item in row)

def test_csv_reader_with_filter():
    data = csv_reader.csv_parser('tests/fixtures/products.csv', filter='rating=4.8')
    with open('tests/fixtures/products.csv', 'r') as file:
        reader = csv.reader(file)
        assert all(item in data for item in list(reader)[2])

def test_csv_reader_with_aggregator():
    data = csv_reader.csv_parser('tests/fixtures/products.csv', aggregator="rating=avg")
    assert "avg" in data
    assert "4.67" in data

def test_csv_reader_all():
    data = csv_reader.csv_parser('tests/fixtures/products.csv', filter="brand=xiaomi", aggregator="rating=min")
    assert "min" in data
    assert "4.4" in data

def test_csv_reader_with_filter_error():
    with pytest.raises(ValueError):
        csv_reader.csv_parser('tests/fixtures/products.csv', filter='rating!4.8')

def test_csv_reader_with_aggregator_empty():
    data = csv_reader.csv_parser('tests/fixtures/products_error.csv', aggregator="rating=avg")
    assert data == ''