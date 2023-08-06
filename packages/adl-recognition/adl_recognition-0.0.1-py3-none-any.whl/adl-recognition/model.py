from keras.models import model_from_json


def getModel(path):
    json_file = open(path+'.json', 'r')
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    # load weights into new model
    model.load_weights(path+".h5")
    return model
