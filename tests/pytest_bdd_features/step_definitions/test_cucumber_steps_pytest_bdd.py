from pytest_bdd import scenario, given, when, then, parsers

EXTRA_TYPES = {
    'Number': int,
}


@given(parsers.parse('I playout "{asset}"'), target_fixture='cli')
def playout(asset, capsys):
    pass


@given(parsers.cfparse('the basket has "{initial:Number}" cucumbers', extra_types=EXTRA_TYPES))
@given('the basket has "<initial>" cucumbers')
def basket(initial):
    pass


@when(parsers.cfparse('"{some:Number}" cucumbers are added to the basket', extra_types=EXTRA_TYPES))
@when('"<some>" cucumbers are added to the basket')
def add_cucumbers(basket, some):
    pass


@when(parsers.cfparse('"{some:Number}" cucumbers are removed from the basket', extra_types=EXTRA_TYPES))
@when('"<some>" cucumbers are removed from the basket')
def remove_cucumbers(basket, some):
    pass


@then(parsers.cfparse('the basket contains "{total:Number}" cucumbers', extra_types=EXTRA_TYPES))
@then('the basket contains "<total>" cucumbers')
def basket_has_total(basket, total):
    pass
