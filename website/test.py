from intasend import APIService

API_PUBLISHABLE_KEY = 'ISPubKey_test_67eb8fd0-d2e0-408f-9675-ec4e9ad18602'
API_TOKEN = 'ISSecretKey_test_f8154bce-546a-44b4-a123-2ade0c21f2cf'

service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

create_order = service.collect.mpesa_stk_push(phone_number='2547377064499', email='johndoe.tes818@gmail.com', amount=5, narrative='Dolbel Order')

# Assuming your original dictionary is stored in a variable named 'invoice_data'



print(create_order)