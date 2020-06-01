import requests

string = "addMe :: Integer -> Integer -> Integer\naddMe x y = x + y\nmain :: IO ()\nmain =  do\nputStr \"Sum of x + y = \"\nprint(addMe 10 25)"

response = requests.post('https://api.jdoodle.com/v1/execute', json={'clientId': "e3762b799cdb4c3ee07e092f6041ce08", 'clientSecret': '123904cc5aa37569cb7fecc393154e7e4d9d3375d08932ef4f7109affd2dda6b', 'script': string, 'stdin': "",'language':"haskell", 'versionIndex':'0'})
 
print (response)