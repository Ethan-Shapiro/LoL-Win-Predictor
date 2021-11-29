prediction = {"blah": 11}
predictions = [prediction.copy(), prediction.copy(), prediction.copy()]

print(predictions)

predictions[0]['blah'] = 12

print(predictions)
