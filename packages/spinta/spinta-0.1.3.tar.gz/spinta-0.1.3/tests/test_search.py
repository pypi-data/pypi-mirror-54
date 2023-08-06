import pytest

from spinta.testing.utils import get_error_codes, get_error_context


test_data = [
    {
        '_type': 'report',
        'status': 'ok',
        'report_type': 'stv',
        'count': 10,
        'notes': [{
            'note': 'hello',
            'note_type': 'simple',
            'create_date': '2019-03-14',
        }],
        'operating_licenses': [{
            'license_types': ['valid'],
        }],
    },
    {
        '_type': 'report',
        'status': 'invalid',
        'report_type': 'vmi',
        'count': 42,
        'notes': [{
            'note': 'world',
            'note_type': 'daily',
            'create_date': '2019-04-20',
        }],
        'operating_licenses': [{
            'license_types': ['expired'],
        }],
    },
    {
        '_type': 'report',
        'status': 'invalid',
        'report_type': 'stv',
        'count': 13,
        'notes': [{
            'note': 'foo bar',
            'note_type': 'important',
            'create_date': '2019-02-01',
        }],
    },
]


def _push_test_data(app, model):
    app.authmodel(model, ['insert'])
    resp = app.post('/', json={'_data': [
        {
            **data,
            '_op': 'insert',
            '_type': model,
        }
        for data in test_data
    ]})
    assert resp.status_code == 200, resp.json()
    resp = resp.json()
    assert '_data' in resp, resp
    return resp['_data']


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
#     'backends/postgres/report/:dataset/test'
# )
@pytest.mark.models(
    'backends/mongo/report',
    'backends/postgres/report/:dataset/test'
)
def test_search_exact(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # single field search
    resp = app.get(f'/{model}?status=ok')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']

    # single field search, case-insensitive
    resp = app.get(f'/{model}?status=OK')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']

    # single field search, non string type
    resp = app.get(f'/{model}?count=13')
    data = resp.json()['_data']

    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # single field fsearch, non string type
    resp = app.get(f'/{model}?count=abc')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["InvalidValue"]

    # single non-existing field value search
    resp = app.get(f'/{model}?status=o')
    data = resp.json()['_data']
    assert len(data) == 0

    # single non-existing field search
    resp = app.get(f'/{model}?state=o')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["FieldNotInResource"]

    # multple field search
    resp = app.get(f'/{model}?status=invalid&report_type=stv')
    data = resp.json()['_data']

    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # same field searched multiple times is joined with AND operation by default
    resp = app.get(f'/{model}?status=invalid&status=ok')
    data = resp.json()['_data']
    assert len(data) == 0


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
# )
@pytest.mark.models(
    'backends/mongo/report',
)
def test_search_gt(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # single field search
    resp = app.get(f'/{model}?count=gt=40')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # search for string value
    resp = app.get(f'/{model}?status=gt=ok')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["InvalidOperandValue"]
    assert get_error_context(
        resp.json(), "InvalidOperandValue", ["operator", "model", "property"]
    ) == {
        "operator": "gt",
        "model": model,
        "property": "status",
    }

    # multi field search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=gt=40&count=gt=10')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # multi field and multi operator search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=gt=40&report_type=vmi')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # test `greater_than` works as expected
    resp = app.get(f'/{model}?count=gt=42')
    data = resp.json()['_data']
    assert len(data) == 0


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
# )
@pytest.mark.models(
    'backends/mongo/report',
)
def test_search_gte(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # single field search
    resp = app.get(f'/{model}?count=ge=40')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # search for string value
    resp = app.get(f'/{model}?status=ge=ok')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["InvalidOperandValue"]
    assert get_error_context(
        resp.json(), "InvalidOperandValue", ["operator", "model", "property"]
    ) == {
        "operator": "ge",
        "model": model,
        "property": "status",
    }

    # multi field search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=ge=40&count=gt=10')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # multi field and multi operator search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=ge=40&report_type=vmi')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # test `greater_than` works as expected
    resp = app.get(f'/{model}?count=ge=42')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
# )
@pytest.mark.models(
    'backends/mongo/report',
)
def test_search_lt(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # single field search
    resp = app.get(f'/{model}?count=lt=12')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']

    # search for string value
    resp = app.get(f'/{model}?status=lt=ok')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["InvalidOperandValue"]
    assert get_error_context(
        resp.json(), "InvalidOperandValue", ["operator", "model", "property"]
    ) == {
        "operator": "lt",
        "model": model,
        "property": "status",
    }

    # multi field search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=lt=20&count=gt=10')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # multi field and multi operator search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=lt=50&report_type=vmi')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # test `lower_than` works as expected
    resp = app.get(f'/{model}?count=lt=10')
    data = resp.json()['_data']
    assert len(data) == 0


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
# )
@pytest.mark.models(
    'backends/mongo/report',
)
def test_search_lte(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # single field search
    resp = app.get(f'/{model}?count=le=12')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']

    # search for string value
    resp = app.get(f'/{model}?status=le=ok')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["InvalidOperandValue"]
    assert get_error_context(
        resp.json(), "InvalidOperandValue", ["operator", "model", "property"]
    ) == {
        "operator": "le",
        "model": model,
        "property": "status",
    }

    # multi field search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=le=20&count=gt=10')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # multi field and multi operator search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=le=50&report_type=vmi')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # test `lower_than` works as expected
    resp = app.get(f'/{model}?count=le=10')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
# )
@pytest.mark.models(
    'backends/mongo/report',
)
def test_search_ne(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # single field search
    resp = app.get(f'/{model}?status=ne=invalid')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']

    # single field search, case insensitive
    resp = app.get(f'/{model}?status=ne=invAlID')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']

    # multi field search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?count=ne=10&count=ne=42')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # multi field and multi operator search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?status=ne=ok&report_type=vmi')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
# )
@pytest.mark.models(
    'backends/mongo/report',
)
def test_search_contains(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # single field search
    resp = app.get(f'/{model}?contains(report_type,vm)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # single field search, case insensitive
    resp = app.get(f'/{model}?contains(report_type,vM)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # multi field search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?contains(status,valid)&contains(report_type,tv)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # multi field search, case insensitive
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?contains(status,vAlId)&contains(report_type,TV)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # multi field search
    # test if operators are joined with AND logic for same field
    resp = app.get(f'/{model}?contains(report_type,vm)&contains(report_type,mi)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # multi field and multi operator search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?contains(status,valid)&report_type=vmi')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # `contains` type check
    resp = app.get(f'/{model}?contains(notes.create_date,2019-04-20)')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["InvalidOperandValue"]
    assert get_error_context(
        resp.json(), "InvalidOperandValue", ["operator", "model", "property"]
    ) == {
        "operator": "contains",
        "model": model,
        "property": "notes.create_date",
    }


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
# )
@pytest.mark.models(
    'backends/mongo/report',
)
def test_search_startswith(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # single field search
    resp = app.get(f'/{model}?startswith(report_type,vm)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # single field search, case insensitive
    resp = app.get(f'/{model}?startswith(report_type,Vm)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # multi field search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?startswith(status,in)&startswith(report_type,vm)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # multi field and multi operator search
    # test if operators are joined with AND logic
    resp = app.get(f'/{model}?startswith(report_type,st)&status=ok')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']

    # sanity check that `startswith` searches from the start
    resp = app.get(f'/{model}?startswith(status,valid)')
    data = resp.json()['_data']
    assert len(data) == 0

    # `startswith` type check
    resp = app.get(f'/{model}?startswith(notes.create_date,2019-04-20)')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["InvalidOperandValue"]


# FIXME: postgres nested objects
# @pytest.mark.models(
#     'backends/mongo/report',
#     'backends/postgres/report',
# )
@pytest.mark.models(
    'backends/mongo/report',
)
def test_search_nested(model, context, app):
    r1, r2, r3, = _push_test_data(app, model)

    app.authmodel(model, ['search'])

    # nested `exact` search
    resp = app.get(f'/{model}?(notes,note)=foo bar')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # nested `exact` search, case insensitive
    resp = app.get(f'/{model}?(notes,note)=foo BAR')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    # nested `gt` search
    resp = app.get(f'/{model}?(notes,create_date)=gt=2019-04-01')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']

    # nested non existant field
    resp = app.get(f'/{model}?(notes,foo,bar)=baz')
    assert resp.status_code == 400
    assert get_error_codes(resp.json()) == ["FieldNotInResource"]
    assert get_error_context(
        resp.json(),
        "FieldNotInResource",
        ["property", "model"]
    ) == {
        "property": "notes.foo.bar",
        "model": model,
    }

    # nested `contains` search
    resp = app.get(f'/{model}?contains(notes.note,bar)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    resp = app.get(f'/{model}?contains(operating_licenses.license_types,lid)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r1['_id']

    # nested `startswith` search
    resp = app.get(f'/{model}?startswith(notes.note,fo)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r3['_id']

    resp = app.get(f'/{model}?startswith(operating_licenses.license_types,exp)')
    data = resp.json()['_data']
    assert len(data) == 1
    assert data[0]['_id'] == r2['_id']
