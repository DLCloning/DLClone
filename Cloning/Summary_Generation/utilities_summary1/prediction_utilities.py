
from utilities_summary1.prediction_cluster_class import Prediction, Cluster

def add_predictions_metrics(predictions, mapping_file, is_perfect, CC, length):
    '''
    for each prediction add some metrics about predictions
    '''
    map_method=dict() # masked method -> method
    for x in mapping_file:
        parts=x.split("|||")
        map_method[parts[0]]=parts[1]

    length_dict=dict() # method -> length
    for x in length:
        parts=x.split("|||")
        length_dict[parts[0]]=parts[1]      

    for i, (x,y) in enumerate(zip(is_perfect, CC)):

        curr_prediction=Prediction(i, x, y)

        curr_prediction.add_length(i, map_method, length_dict)
        predictions[i]=curr_prediction

    return predictions

def add_prediction_and_target(predictions, prediction_lines, prediction_map, target_lines, target_map):
    '''
    for each prediction add the prediction lines and the target lines
    '''
    for key in predictions.keys():

        start_method, end_method= prediction_map[key]

        all_lines_prediction=(prediction_lines[(start_method):(end_method+1)])

        start_method, end_method= target_map[key]

        all_lines_target=(target_lines[(start_method):(end_method+1)])

        predictions[key].add_prediction_target(all_lines_prediction, all_lines_target)

    return predictions

def add_unknown_token_and_line_masked(predictions, dict_unknown, mask_length):
    '''
    for each prediction add the prediction lines and the target lines
    '''
    for key in predictions.keys():

        if key in dict_unknown.keys():
            predictions[key].set_unknown(True)

        else:
            predictions[key].set_unknown(False)

        predictions[key].set_length_mask(int(mask_length[key]))

    return predictions

def add_confidence(predictions, confidence):
    '''
    for each prediction add the confidence of the model on the prediction
    '''
    for i, key in enumerate(predictions.keys()):

        predictions[key].set_confidence(float(confidence[i]))

    return predictions


def is_prediction(name):
    if "prediction" in name:
        return True

    return False