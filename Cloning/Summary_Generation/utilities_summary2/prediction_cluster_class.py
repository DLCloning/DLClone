from utilities_summary2.excel_API import *

dict_key=dict()
dict_key[True]="prediction"
dict_key[False]="target"

class Prediction():
    '''
    class for the prediction
    '''
    def __init__(self, id_prediction, is_perfect, CC):
        self.id=id_prediction # id of the prediction (from 0 to len(prediction))
        self.clusters=list() # clusters that contain the specific prediction (e.g. [24, 55])

        # is perfect prediction of not
        self.is_perfect=False
        if str(is_perfect).lower()=="true":
            self.is_perfect=True

        if CC is not None:
            # cyclomatic complexity of the entire method 
            # and of the method without the mask (the context seen by the model for predicting)
            parts=CC.split("|||")
            self.CC_method=int(parts[1]) # CC of the entire method
            self.CC_nomask=int(parts[2]) # CC of the entire method without the masked part
        # prediction code and target code
        self.prediction_lines=list()
        self.target_lines=list()

    def clone(self):
        p_clone=Prediction(self.id, self.is_perfect, None)
        p_clone.CC_method=self.CC_method
        p_clone.CC_nomask=self.CC_nomask
        p_clone.prediction_lines=self.prediction_lines.copy()
        p_clone.target_lines=self.target_lines.copy()
        p_clone.num_lines=self.num_lines
        p_clone.clusters=self.clusters.copy()
        p_clone.unknown_token=self.unknown_token
        p_clone.num_mask_line=self.num_mask_line
        p_clone.confidence=self.confidence
        return p_clone


    def add_length(self, id_curr, map_method, length_dict):
        '''
        add the number of lines of the test method.
        this measure the complexity of the context seen by the model
        '''
        masked_method_id=list(map_method.keys())[id_curr]
        method_id=map_method[masked_method_id]
        length=length_dict[method_id]
        self.num_lines=int(length)
        # print("method with id {}, masked method id {} and method id {} has a length of {}".format(id_curr, masked_method_id, method_id, length))

    def add_prediction_target(self, prediction_lines, target_lines):
        '''
        add the prediction code and the target code
        '''
        self.prediction_lines=prediction_lines
        self.target_lines=target_lines

    def add_cluster(self, id_cluster):
        '''
        add a cluster to the clusters list that contain the prediction
        '''
        self.clusters.append(id_cluster)

    def print(self):
        print("Prediction {}, is perfect: {}".format(self.id, self.is_perfect))
        print("{} clusters: {}".format(len(self.clusters), str(self.clusters)))

    def set_unknown(self, unknown):
        '''
        set the unknown token
        '''
        self.unknown_token=unknown

    def set_length_mask(self, lines):
        '''
        set the number of lines that have been masked (from 2 to 6)
        '''
        self.num_mask_line=lines

    def set_confidence(self, confidence):
        '''
        set the confidence of the model for that prediction
        '''
        conf_adjusted=confidence if confidence >= 0.01 else 0
        self.confidence=conf_adjusted

    def compute_average_cluster_size(self, clusters_dict):
        '''
        compute the average number of method that are present in the cluster
        we count pretraining, training method and prediction blocks
        '''
        num_clusters=len(self.clusters)
        if num_clusters == 0:
            return 0
        tot_elements=0
        for cluster_key in self.clusters:
            cluster=clusters_dict[cluster_key]
            tot_elements+=len(set(cluster.pretraining))
            tot_elements+=len(set(cluster.predictions))
            tot_elements+=len(set(cluster.training))

        return int(tot_elements/num_clusters)

    def write_excel_line(self, line_id, sheet, clusters_dict, num_cluster_1):
        '''
        write a single line in the excel containing all reported information about cluster 1
        '''

        distinct_clusters=list(set(self.clusters))
        average_size_cluster=self.compute_average_cluster_size(clusters_dict)


        fill_cells(sheet, ["A{}".format(line_id),"B{}".format(line_id), "C{}".format(line_id), "D{}".format(line_id), 
            "E{}".format(line_id), "F{}".format(line_id), "G{}".format(line_id), "H{}".format(line_id)],
            [self.id, str(self.is_perfect), self.CC_method, self.CC_nomask, self.num_lines, self.num_mask_line, 
            str(self.unknown_token), self.confidence])

        fill_cells(sheet, ["I{}".format(line_id), "J{}".format(line_id)], ["\n".join(self.prediction_lines), "\n".join(self.target_lines)])
        fill_cells(sheet, ["K{}".format(line_id)], [len(distinct_clusters)])
        fill_cells(sheet, ["L{}".format(line_id)], [num_cluster_1])
        fill_cells(sheet, ["M{}".format(line_id)], [average_size_cluster])
            
        wrap_text(sheet, "I{}".format(line_id))
        wrap_text(sheet, "J{}".format(line_id))


class Oracle():
    '''
    class for the oracles
    '''
    def __init__(self, id_oracle):
        self.id=id_oracle # id of the oracle (from 0 to len(prediction))
        self.clusters=list() # clusters that contain the specific prediction (e.g. [24, 55])


    def clone(self):
        o_cloned=Oracle(self.id)
        o_cloned.clusters=self.clusters.copy()
        return o_cloned

    def add_cluster(self, id_cluster):
        '''
        add a cluster to the clusters list that contain the prediction
        '''
        self.clusters.append(id_cluster)

    def print(self):
        print("Oracle {}".format(self.id))
        print("{} clusters: {}".format(len(self.clusters), str(self.clusters)))


    def compute_average_cluster_size(self, clusters_dict):
        '''
        compute the average number of method that are present in the cluster
        we count pretraining, training method and oracle blocks
        '''
        num_clusters=len(self.clusters)
        if num_clusters == 0:
            return 0
        tot_elements=0
        for cluster_key in self.clusters:
            cluster=clusters_dict[cluster_key]
            tot_elements+=len(set(cluster.pretraining))
            tot_elements+=len(set(cluster.predictions))
            tot_elements+=len(set(cluster.training))

        return int(tot_elements/num_clusters)


class Cluster():

    def __init__(self, id_cluster, num_lines):
        self.id=id_cluster # id of the cluster (from 0 to the total number of clusters found by Simian)
        self.num_lines=num_lines # number of lines of the cluster
        self.pretraining=list() #id of the pretraining method contained in the cluster
        self.training=list() #id of the training method contained in the cluster
        self.predictions=list() #id of the prediction blocks contained in the cluster

    def clone(self):
        c_cloned=Cluster(self.id, self.num_lines)
        c_cloned.pretraining=self.pretraining.copy()
        c_cloned.training=self.training.copy()
        c_cloned.predictions=self.predictions.copy()
        return c_cloned

    def add_element(self, id_file, file_name, is_prediction_file):
        '''
        add the element in pretraining, training or prediction/target
        '''
        if "pretrain" in file_name:
            self.pretraining.append(id_file)
        elif dict_key[is_prediction_file] in file_name:
            self.predictions.append(id_file)
        else:
            self.training.append(id_file)


    def print(self):
        '''
        print cluster information
        '''
        print("Cluster {} of {} lines".format(self.id, self.num_lines))
        print("{} pretraining methods occurrences".format(len(self.pretraining)))
        print("{} training methods occurrences".format(len(self.training)))
        print("{} prediction methods occurrences".format(len(self.predictions)))