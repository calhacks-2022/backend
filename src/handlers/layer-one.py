import sys
sys.path.insert(0, 'src/vendor')
import json
import requests
import cohere
import os

def search_npm(api_key, queries):
    ret = set()
    for query in queries:
        r = requests.get(f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx=626e50bc7dd2043a2&q={query}&fields=items(link)")
        res = r.json()
        if 'items' not in res:
            print("Error")
            print(queries)
            return []
        results = [item['link'].split('package/')[-1].split('/v/')[0] for item in res['items']]
        for result in results:
            ret.add(result)
    return list(ret)

def get_recommendations(api_key, query):
    co = cohere.Client(api_key)
    response = co.generate(
    model='large',
    prompt='User: What is the best react library that I can install and use for making UI components in React?\nList:@mui/material \nantd \nreactstrap \n@coreui/react \nsemantic-ui-react\n--\n'
        +'User: What is the best library that I can install and use for making API requests in React?\nList:axios\n@types/superagent\nky\npopsicle\nstream-http\n--\n'
        +'User: I want to include some icons\nList:material-design-icons \nfontawesome \nionicons \nreact-native-icons \nocticons \n--\n'
        +'User: I want to install and parse XML to JSON in my React project for school\nList:xml2js \nxml2json \nsimple-xml-to-json \nfast-xml-parser\n@xmldom/xmldom\n--\n'
        +'User: animation components\nList: reactstrap \nreact-spring \nreact-move \nremotion\nframer-motion\n--\n'
        +'User: dropdown\nList:downshift\nreact-single-dropdown\nreact-select-search\nreact-dropdown-tree-select\nreact-multi-select-component\n--\n'
        +'User: data visualization\nList:react-chartjs-2\nrecharts\nvictory\n@visx/visx\nnivo\n--\n'
        +'User: countdown timer\nList:react-timer-component\nreact-timer\nreact-countdown\n--\n'
        +'User: '
        + query
        + '\nList:',
    max_tokens=100,
    temperature=0.8,
    k=0,
    p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=["--"],
    return_likelihoods='NONE')
    return response.generations[0].text.split("\n")[:-1]

def main(event, context):
    print(os.environ)

    res = json.loads(event.get("body"))
    userQuery = res.get("query", "")

    if not userQuery:
        return {
            'statusCode': 400,
            'body': 'Missing query'
        }

    COHERE_API = os.environ["COHERE_API"]
    GOOGLE_API = os.environ["GOOGLE_API"]

    cohere_suggestions = get_recommendations(COHERE_API, userQuery)
    plausible_packages = search_npm(GOOGLE_API, cohere_suggestions)

    return {
        'statusCode': 200,
        'body': json.dumps({"data": plausible_packages}),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
            'Access-Control-Allow-Origin': '*',
        },
    }

if __name__ == "__main__":
    main('', '')