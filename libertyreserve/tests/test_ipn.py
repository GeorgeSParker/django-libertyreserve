from django.conf import settings
from django.test import TestCase
 
from libertyreserve.models import LibertyReserveIPN
from libertyreserve.signals import (payment_was_successful,
    payment_was_flagged)
 
IPN_POST_PARAMS = {
    "lr_paidto": "X1234567",
    "lr_paidby": "U789",
    "lr_amnt": "12.34",
    "lr_fee_amnt": "0",
    "lr_currency": "LRUSD",
    "lr_transfer": "4456778335534",
    "lr_store": "MyStore",
    "lr_timestamp": "2007-25-03 10:45:55",
    "lr_merchant_ref": "HGF44556756",
    "lr_encrypted": "E71A1EE0A1396EDB03FD24BE88C129CFE3DFFC8A05188084FB853305978080FB",
    "lr_encrypted2": "9AF94F87C696E9A51869DDA98C8B3ED45A3ED46E434939348664CED77A6DAD90",
}
 
class IPNTest(TestCase):
    urls = 'libertyreserve.tests.test_urls'
 
    def setUp(self):
        self.old_debug = settings.DEBUG
        self.old_libertyreserve_account = settings.LIBERTYRESERVE_ACCOUNT
        self.old_libertyreserve_secret = settings.LIBERTYRESERVE_SECRET
        settings.DEBUG = True
        settings.LIBERTYRESERVE_ACCOUNT = 'X1234567'
        settings.LIBERTYRESERVE_SECRET = 'secretsecretsecret'
        
    def tearDown(self):
        settings.DEBUG = self.old_debug
        settings.LIBERTYRESERVE_ACCOUNT = self.old_libertyreserve_account
        settings.LIBERTYRESERVE_SECRET = self.old_libertyreserve_secret
 
    def assertGotSignal(self, signal, flagged, url='/ipn/'):
        # Check the signal was sent. These get lost if they don't reference self.
        self.got_signal = False
        self.signal_obj = None
        
        def handle_signal(sender, **kwargs):
            self.got_signal = True
            self.signal_obj = sender
        signal.connect(handle_signal)
        
        response = self.client.post(url, IPN_POST_PARAMS)
        self.assertEqual(response.status_code, 200)
        ipns = LibertyReserveIPN.objects.all()
        self.assertEqual(len(ipns), 1)
        ipn_obj = ipns[0]
        self.assertEqual(ipn_obj.flag, flagged)
        
        self.assertTrue(self.got_signal)
        self.assertEqual(self.signal_obj, ipn_obj)
        
    def test_correct_ipn(self):
        self.assertGotSignal(payment_was_successful, False)

    def test_correct_ipn_custom(self):
        self.assertGotSignal(payment_was_successful, False, url='/ipn_verify_custom/')

    def test_failed_ipn_custom(self):
        self.assertGotSignal(payment_was_flagged, True, url='/ipn_fail_custom/')

    def assertFlagged(self, updates, flag_info, url='/ipn/'):
        params = IPN_POST_PARAMS.copy()
        params.update(updates)
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, 200)
        ipn_obj = LibertyReserveIPN.objects.all()[0]
        self.assertEqual(ipn_obj.flag, True)
        self.assertEqual(ipn_obj.flag_info, flag_info)
 
    def test_incorrect_account(self):
        update = {"lr_paidto": "X7654321"}
        flag_info = "Invalid lr_paidto. (X7654321)"
        self.assertFlagged(update, flag_info, url='/ipn_verify_custom/')

    def test_incorrect_secret(self):
        update = {"lr_encrypted2": "E71A1EE0A1396EDB03FD24BE88C129CFE3DFFC8A05188084FB853305978080FB"}
        flag_info = "Invalid lr_encrypted2. (E71A1EE0A1396EDB03FD24BE88C129CFE3DFFC8A05188084FB853305978080FB)"
        self.assertFlagged(update, flag_info)

    def test_incorrect_amount(self):
        update = {"lr_amnt": "100.00", "lr_encrypted2": "1E5B50C1268D49DCDAF3356228B574A1F278E5E17D03F17B9FABDBA924FD7805"}
        flag_info = "Invalid lr_amnt. (100.00)"
        self.assertFlagged(update, flag_info, url='/ipn_verify_custom/')

    def test_incorrect_currency(self):
        update = {"lr_currency": "LREUR", "lr_encrypted2": "BE9A2232FF86D2A9E0E4D080CCCEF3C620E618D1BBBFB34D90B7776CEDA6185B"}
        flag_info = "Invalid lr_currency. (LREUR)"
        self.assertFlagged(update, flag_info, url='/ipn_verify_custom/')
 
    def test_duplicate_transfer_id(self):
        self.client.post("/ipn/", IPN_POST_PARAMS)
        self.client.post("/ipn/", IPN_POST_PARAMS)
        self.assertEqual(len(LibertyReserveIPN.objects.all()), 2)
        ipn_obj = LibertyReserveIPN.objects.order_by('-created_at')[0]
        self.assertEqual(ipn_obj.flag, True)
        self.assertEqual(ipn_obj.flag_info, "Duplicate lr_transfer. (4456778335534)")

