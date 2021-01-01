# aws-lambda-model

## Description

Built an API to run small machine learning models using AWS SAM.

## Testing and Deployment

See [AWS SAM CLI doc](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)

## Usage

An example to use the API to collect multiple results:

```JavaScript
function getPredictionResultsPromise() {
  // The input can predict an output for each model type
  const ids = [
    'inputGroupSelectEducation',
    'inputGroupSelectEmployment',
    'inputGroupSelectMarijuana',
    'inputGroupSexualId',
    'inputGroupHealth',
    'inputGroupEduDrugs',
    'inputGroupGrade',
    'inputGroupAttack',
    'inputGroupReligious'
  ];

  // The model types
  const modelTypes = [
    'alcohol',
    'cocever',
    'crkever',
    'herever',
    'impsoc',
    'metha',
    'tobacco',
    'impwork'
  ];

  // Get the input values
  const input = ids.reduce((prev, id) => {
    prev.push(+document.getElementById(id).value);
    return prev;
  }, []);

  return new Promise((resolve, reject) => {
    Promise.all(modelTypes.reduce((prev, type) => {
        prev.push(new Promise((resolve, reject) => {
          const url = new URL('YOUR DEPLOYED ENDPOINT');
          url.search = new URLSearchParams({
            type: type,
            input: JSON.stringify(input)
          }).toString();
          fetch(url)
            .then(response => response.ok ? response.json() : Promise.reject(response))
            .then(json => resolve({
              key: type,
              value: +json.output
            }))
            .catch(error => reject(error));
        }));
        return prev;
      }, []))
      .then(values => resolve(values.reduce((prev, curr) => {
        prev[curr.key] = curr.value;
        return prev;
      }, {})))
      .catch(e => reject(e));
  });
}
```
