import sys
sys.path.insert(0, 'src/vendor')
import json
import pickle
import numpy as np

def main(event, context):
    res = json.loads(event.get("body"))
    packages = res.get("packages", [])

    pkgs, pkg_samples = pickle.load(open('pkg.pkl', 'rb'))

    pkg_indices = []
    pkg_names = []
    for package in packages:
        try:
            pkg_indices.append(pkgs.index(package))
            pkg_names.append(package)
        except:
            pass

    relevant_encoded_data = np.zeros((len(pkg_samples), len(pkg_indices)))

    for i in range(len(pkg_samples)):
        for j in range((len(pkg_indices))):
            if pkg_indices[j] in pkg_samples[i]:
                relevant_encoded_data[i][j] = 1

    covariance = np.cov(relevant_encoded_data[:, np.arange(len(pkg_names))].T)
    covariance_rounded = np.round(covariance, 5)
    return {
        'statusCode': 200,
        'body': json.dumps({"covariance": covariance_rounded.tolist(), "names": pkg_names}),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
            'Access-Control-Allow-Origin': '*',
        },
    }

if __name__ == "__main__":
    main('', '')
    # res = main({"body": json.dumps({"packages": ['create-react-app', 'dotenv', 'express']})}, '')
    # print(res)
