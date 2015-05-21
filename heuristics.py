import csv
import sys

def extract_features(record):
  return {
    'id': int(record[0]),
    'survived': int(record[1]),
    'gender': record[4]
  }

def parse_test_data(record):
  return {
    'id': int(record[0]),
    'gender': record[3]
  }

def gender_heuristic(record):
  if record['gender'] == 'female':
    return 1
  else:
    return 0

def test_heuristic(heuristic):
  with open('data/train.csv', 'r') as training_data:
    reader = csv.reader(training_data)
    next(reader, None) # skip header

    data_set = [extract_features(record) for record in reader]

    total_records = 0
    matched_records = 0

    for datum in data_set:
      survived = heuristic(datum)

      if survived == datum['survived']:
        matched_records += 1

      total_records += 1

    print "score {}".format((float(matched_records) / float(total_records)))

def generate_submission(heuristic):
  with open('data/test.csv', 'r') as test_data:
    reader = csv.reader(test_data)
    next(reader, None) # skip header

    data_set = [parse_test_data(record) for record in reader]
    results = [(record['id'], heuristic(record)) for record in data_set]

    with open('submission.csv', 'w') as submission:
      writer = csv.writer(submission)
      writer.writerow(('PassengerId', 'Survived'))

      for result in results:
        writer.writerow(result)

    print "Saved submission to submission.csv"


if len(sys.argv) == 2 and sys.argv[1] == 'test':
  test_heuristic(gender_heuristic)
else:
  generate_submission(gender_heuristic)
