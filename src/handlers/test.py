import sys
sys.path.insert(0, 'src/vendor')
import json
import pickle
import numpy as np

def main(event, context):
    print("Event:", event)
    print("Context:", context)

    # try:
    #     pickleData = pickle.load(open('test.pkl', 'rb'))
    #     print(pickleData)
    # except Exception as e:
    #     print(e)

    # try:
    #     print(np.array([1,2,3]))
    # except Exception as e:
    #     print(e)

    return {
        'statusCode': 200,
        'body': json.dumps({"name": "John Doe"})
    }

if __name__ == "__main__":
    main('', '')