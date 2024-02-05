import re
import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

cnt = 0
@transformer
def transform(data, *args, **kwargs):
    
    def to_snake(name):
        if any(c.isupper() for c in name):
            global cnt
            cnt += 1
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        else:
            return name

    data_tmp = data[(data['passenger_count'] != 0) & (data['trip_distance'] != 0)]
    data_tmp['lpep_pickup_date'] = data_tmp['lpep_pickup_datetime'].dt.date

    data_tmp.columns = [to_snake(x) for x in data_tmp.columns]

    unique_vendors = set(data_tmp['vendor_id'])

    print(f'vendor_id unique values are: {unique_vendors}')
    print(f'Number of cols to be transformed into snake case: {cnt}')

    return data_tmp


@test
def test_output(output, *args) -> None:
    assert output['vendor_id'].isin(set(output['vendor_id'])).all()
    assert output['passenger_count'].isin([0]).sum() == 0
    assert output['trip_distance'].isin([0]).sum() == 0
