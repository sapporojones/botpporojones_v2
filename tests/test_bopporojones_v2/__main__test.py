import pytest
import requests


def test_alice():
    alice_name = "TEST"
    alice_srch = requests.get(
        f"https://esi.evetech.net/latest/search/?categories=alliance&datasource=tranquility"
        f"&language=en&search={alice_name}&strict=true"
    )
    alice_srch_json = alice_srch.json()
    if len(alice_srch_json) <= 0:
        raise Exception("Alliance not found")
    else:
        alice_id = alice_srch_json["alliance"][0]

    line1 = "**CORP SEARCH RESULTS:**" + "\n"
    line2 = f"**ZKB:** https://zkillboard.com/alliance/{alice_id}/ \n"
    line3 = f"**EVEWHO:** https://evewho.com/alliance/{alice_id}/ \n"
    line4 = f"**DOTLAN:** http://evemaps.dotlan.net/alliance/{alice_id}/ \n"
    response = line1 + line2 + line3 + line4
    assert len(response) >= 1
