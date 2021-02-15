import unittest 
import requests

class ScriptTest(unittest.TestCase):
    baseURL = 'http://127.0.0.1:5000'

    def test1_transactEther_negative(self):
        transactEtherURL = self.baseURL+'/transact/ether'
        response = requests.post(transactEtherURL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Balance insufficient", response.text)

    def test2_transactEther_positive(self):
        transactEtherURL = self.baseURL+'/transact/etherFromAny'
        response = requests.post(transactEtherURL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Transfer completed successfully", response.text)
        print(response.text)

    def test3_transferCustomerERC20Token_positive(self):
        transferTokenURL = self.baseURL+'/transact/myTKN'
        response = requests.post(transferTokenURL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Transfer completed successfully", response.text)

    def test4_getReportInfo_positive(self):
        address = "0x3794ac09Fa60569e468661d7fd2b3C6F9C1d4D27"
        reportsURL = self.baseURL+'/viewReportJSON/{}'.format(address)
        response = requests.get(reportsURL)
        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertGreaterEqual(len(report), 0)

if __name__ == "__main__":
    unittest.main()
