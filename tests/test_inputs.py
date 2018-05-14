import tax_computation


def test_case_1(capsys):
    with open('files/test1.txt'.format(tax_computation.file_path)) as current_file:
        shopping_cart = tax_computation.context_analysis(text_input=current_file)
    pay_station = tax_computation.PayStation(shopping_cart)
    pay_station.compute_taxes()
    pay_station.compute_total_price()
    pay_station.create_bill()
    output, err = capsys.readouterr()
    output = output.split('\n')
    assert '12.49' in output[0]
    assert '0.85' in output[1]
    assert '16.49' in output[2]
    assert '1.5' in output[3]
    assert '29.83' in output[4]


def test_case_2(capsys):
    with open('files/test2.txt'.format(tax_computation.file_path)) as current_file:
        shopping_cart = tax_computation.context_analysis(text_input=current_file)
    pay_station = tax_computation.PayStation(shopping_cart)
    pay_station.compute_taxes()
    pay_station.compute_total_price()
    pay_station.create_bill()
    output, err = capsys.readouterr()
    output = output.split('\n')
    assert '10.5' in output[0]
    assert '54.65' in output[1]
    assert '7.65' in output[2]
    assert '65.15' in output[3]


def test_case_3(capsys):
    with open('files/test3.txt'.format(tax_computation.file_path)) as current_file:
        shopping_cart = tax_computation.context_analysis(text_input=current_file)
    pay_station = tax_computation.PayStation(shopping_cart)
    pay_station.compute_taxes()
    pay_station.compute_total_price()
    pay_station.create_bill()
    output, err = capsys.readouterr()
    output = output.split('\n')
    assert '32.19' in output[0]
    assert '20.89' in output[1]
    assert '9.75' in output[2]
    assert '11.85' in output[3]
    assert '6.7' in output[4]
    assert '74.68' in output[5]


def test_case_4(capsys):
    with open('files/test4.txt'.format(tax_computation.file_path)) as current_file:
        shopping_cart = tax_computation.context_analysis(text_input=current_file)
    pay_station = tax_computation.PayStation(shopping_cart)
    pay_station.compute_taxes()
    pay_station.compute_total_price()
    pay_station.create_bill()
    output, err = capsys.readouterr()
    output = output.split('\n')
    assert '' in output[0]


def test_case_specials(capsys):
    with open('files/test_specials.txt'.format(tax_computation.file_path)) as current_file:
        shopping_cart = tax_computation.context_analysis(text_input=current_file)
    pay_station = tax_computation.PayStation(shopping_cart)
    pay_station.compute_taxes()
    pay_station.compute_total_price()
    pay_station.create_bill()
    output, err = capsys.readouterr()
    output = output.split('\n')
    assert 'Montant des taxes : 0.0' in output[-3]
    assert 'Total : 0.0' in output[-2]