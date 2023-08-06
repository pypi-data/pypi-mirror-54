import json
import time
import os

import requests
import pandas as pd
from io import StringIO

# default url and api key
service_url='http://127.0.0.1:5000/'
api_key='nothing-special'

# if host_info.dat file found, take host info from it
homedir = os.path.expanduser('~')
hostfile = os.path.join(homedir,'.aionics_key')
if os.path.exists(hostfile):
    with open(hostfile,'r') as f:
        service_url = str(f.readline().strip())
        api_key = str(f.readline().strip())

class Client(object):

    def __init__(self,service_url=service_url,api_key=api_key):
        """Client initializer.

        Parameters
        ----------
        service_url : str
            Web URL pointing to your AIONICS service
        api_key : str
            API authorization key for your AIONICS service
        """
        super(Client,self).__init__()
        test_url = service_url+'test_connection'
        resp = requests.get(test_url, headers={'Api-Key':api_key})
        try:
            if resp.json()['response'] == 'connected to aionics service':
                self.service_url = service_url
                self.api_key = api_key
            else: 
                raise RuntimeError('unexpected response: {}'.format(resp.json()))
        except Exception as ex:
            raise RuntimeError('failed to connect to {} ({})'.format(service_url,ex))

    def compute_poscar_descriptors(self,poscar_path):
        """Compute descriptors from a POSCAR file.

        Parameters
        ----------
        poscar_path : str
            Path to a POSCAR file on your local filesystem

        Returns
        -------
        desc : dict
            Dict containing computed descriptors or error report 
        """
        desc = requests.post(
            self.service_url+'compute_poscar_descriptors',
            files={'poscar':open(poscar_path)},
            headers={'Api-Key':self.api_key}
        )
        return desc.json()

    def get_descriptors_by_mpid(self,mpid):
        """Compute descriptors for a material with a Materials Project id. 

        Parameters
        ----------
        mpid : str
            Materials Project id for the desired material

        Returns
        -------
        desc : dict
            Dict containing computed descriptors or error report
        """
        resp = requests.get(
            self.service_url+'get_descriptors_by_mpid', 
            params={'mpid_query':mpid},
            headers={'Api-Key':self.api_key}
            )
        return resp.json()

    def upload_dataset(self,dataset_path):
        """Upload a new dataset to the server.

        Parameters
        ----------
        dataset_path : str
            Path to csv file containing the dataset on the local filesystem-
            the csv file should contain a column named 'id', 
            and this column should be valid as an index 
            (i.e. it should be unique for all samples in the dataset)

        Returns
        -------
        resp : dict
            Dict containing the new dataset's id or an error report
        """
        resp = requests.post(
            self.service_url+'save_dataset',
            files={'dataset':open(dataset_path)},
            headers={'Api-Key':self.api_key}
            )
        return resp.json()

    def get_dataset(self,dataset_id=0):
        """Get a saved dataset by its id.

        Returns either a dataset (as a pandas.DataFrame) if the query is successful,
        or an error report (as a dict) if the query fails.

        Parameters
        ----------
        dataset_id : int
            Integer index of the desired dataset

        Returns
        -------
        ds : pandas.DataFrame 
            DataFrame containing the dataset
        resp : dict
            Dict containing an error report 
        """
        resp = requests.get(
            self.service_url+'get_dataset',
            params={'dataset_id':dataset_id},
            headers={'Api-Key':self.api_key}
            )
        if 'error' in resp._content.decode():
            return resp.json()
        else:
            ds = pd.read_csv(StringIO(resp._content.decode()),index_col='id')
            return ds

    def get_descriptors_from_sample(self,dataset_id,sample_id):
        """Get the descriptors of a sample from a saved dataset.

        Parameters
        ----------
        dataset_id : int
            Integer index of the desired dataset
        sample_id : str
            String id of the desired sample

        Returns
        -------
        desc : dict
            Dict containing the sample descriptors or an error report
        """
        desc = requests.get(
            self.service_url+'get_descriptors_from_sample', 
            params={'dataset_id':dataset_id,'sample_id':sample_id},
            headers={'Api-Key':self.api_key}
            )
        return desc.json()

    def delete_dataset(self,dataset_id):
        """Delete a dataset.

        Deletes the dataset from the index 
        and wipes out all existing files associated with the dataset.
        This cannot be undone.

        Parameters
        ----------
        dataset_id : int
            Integer index of the dataset to delete

        Returns
        -------
        resp : dict
            Report of success or failure in deleting the dataset
        """
        resp = requests.get(
            self.service_url+'delete_dataset', 
            params={'dataset_id':dataset_id},
            headers={'Api-Key':self.api_key}
            )
        return resp.json()

    def run_logreg_combo_selection(self,dspath_or_dsid,min_feats,max_feats,input_keys,output_key,penalty='none',C=1.):
        """Run combinatoric feature selection for a logistic regression model.

        Parameters
        ----------
        dspath_or_dsid : str or int
            Either a path to a csv file on the local filesystem (for using a local dataset),
            or an integer dataset index for the desired dataset (for using a saved dataset)
        min_feats : int
            Minimum number of features to investigate
        max_feats : int
            Maximum number of features to investigate
        input_keys : list
            Dataset columns to include as inputs (descriptors are selected from among these)
        output_key : str
            Column to use as the model output (must be a categorical column)
        penalty : str
            Penalty function for regularization ('none', 'l1', or 'l2')
        C : float
            Penalty term (high values of C effectively lead to lower regularization strength)

        Returns
        -------
        resp : dict
            Dict containing either combinatoric selection results or an error report
        """
        if isinstance(dspath_or_dsid,int):
            resp = requests.get(
                self.service_url+'run_logreg_cfs_by_dsid',
                params={'dataset_id':dspath_or_dsid,'min_feats':min_feats,'max_feats':max_feats,'input_keys':json.dumps(input_keys),'output_key':output_key,'penalty':penalty,'C':C},
                headers={'Api-Key':self.api_key}
                )
        elif isinstance(dspath_or_dsid,str):
            resp = requests.post(
                self.service_url+'run_logreg_cfs_from_data',
                files={'dataset':open(dspath_or_dsid)},
                params={'min_feats':min_feats,'max_feats':max_feats,'input_keys':json.dumps(input_keys),'output_key':output_key,'penalty':penalty,'C':C},
                headers={'Api-Key':self.api_key}
                )
        return resp.json()

    def train_logistic_regression(self,dspath_or_dsid,input_keys,output_key,penalty='none',C=1.):
        """Train a logistic regression model.

        Parameters
        ----------
        dspath_or_dsid : str or int
            Either a path to a csv file on the local filesystem (for using a local dataset),
            or an integer dataset index for the desired dataset (for using a saved dataset)
        input_keys : list
            Dataset columns to include as inputs (descriptors are selected from among these)
        output_key : str
            Column to use as the model output (must be a categorical column)
        penalty : str
            Penalty function for regularization ('none', 'l1', or 'l2')
        C : float
            Penalty term (high values of C effectively lead to lower regularization strength)

        Returns
        -------
        resp : dict
            Dict containing new model id and training results, or error report
        """
        if isinstance(dspath_or_dsid,int):
            resp = requests.get(
                self.service_url+'train_logreg_from_dsid',
                params={'dataset_id':dspath_or_dsid,'input_keys':json.dumps(input_keys),'output_key':output_key,'penalty':penalty,'C':C},
                headers={'Api-Key':self.api_key}
                )
        elif isinstance(dspath_or_dsid,str):
            resp = requests.post(
                self.service_url+'train_logreg_from_data',
                files={'dataset':open(dspath_or_dsid)},
                params={'input_keys':json.dumps(input_keys),'output_key':output_key,'penalty':penalty,'C':C},
                headers={'Api-Key':self.api_key}
                )
        return resp.json()

    def delete_model(self,model_id):
        """Delete a model by providing its id.

        Deletes the model from the index 
        and wipes out all existing files associated with the model.
        This cannot be undone.

        Parameters
        ----------
        model_id : int
            Integer id of the model to be deleted.

        Returns
        -------
        resp : dict
            Dict reporting success or failure in deleting the model.
        """
        resp = requests.get(
            self.service_url+'delete_model', 
            params={'model_id':model_id},
            headers={'Api-Key':self.api_key}
            )
        return resp.json()

    def apply_model(self,model_id,sample):
        """Apply a model to a sample by providing its descriptors.

        Parameters
        ----------
        model_id : int
            Integer id of the model to be applied
        sample : dict
            Dict containing sample descriptors (must be the correct descriptors for the model)

        Returns
        -------
        resp : dict
            Dict containing model result or error report
        """
        resp = requests.get(
                self.service_url+'apply_model',
                params={'model_id':model_id,'sample':json.dumps(sample)},
                headers={'Api-Key':self.api_key}
                )
        return resp.json()

    def apply_model_to_mpid(self,model_id,mpid):
        """Apply a model to a sample by providing the Materials Project id of the sample.

        Parameters
        ----------
        model_id : int
            Integer id of the model to be applied
        mpid : str
            Materials Project id of the material to be evaluated

        Returns
        -------
        resp : dict
            Dict containing model result or error report
        """
        resp = requests.get(
                self.service_url+'apply_model_to_mpid',
                params={'model_id':model_id,'mpid':mpid},
                headers={'Api-Key':self.api_key}
                )
        return resp.json()

    def apply_model_to_sample(self,model_id,dataset_id,sample_id):
        """Apply a model to a sample from a saved dataset.

        Parameters
        ----------
        model_id : int
            Integer id of the model ot be applied
        dataset_id : int
            Integer id of the dataset containing the sample of interest
        sample_id : str
            id (from the dataset index) of the sample to be evaluated

        Returns
        -------
        resp : dict
            Dict containing model result or error report
        """
        resp = requests.get(
                self.service_url+'apply_model_to_sample',
                params={'model_id':model_id,'dataset_id':dataset_id,'sample_id':sample_id},
                headers={'Api-Key':self.api_key}
                )
        return resp.json()

    def apply_model_to_poscar(self,model_id,poscar_path):
        """Compute descriptors from a POSCAR file.

        Parameters
        ----------
        model_id : int
            Integer id of the model ot be applied
        poscar_path : str
            Path to a poscar file on the local filesystem

        Returns
        -------
        resp : dict
            Dict containing model result or error report
        """
        resp = requests.post(
                self.service_url+'apply_model_to_poscar',
                files={'poscar':open(poscar_path)},
                params={'model_id':model_id},
                headers={'Api-Key':self.api_key}
                )
        return resp.json()

    def get_logreg_combo_results(self,process_id,wait=False):
        """Fetch results of logistic regression combinatoric feature selection

        Parameters
        ----------
        process_id : int
            Integer id assigned to the feature selection process
            when it was initially launched
        wait : bool
            If True, the client will attempt to retrieve the result repeatedly,
            until the result is successfully returned.
            If False, the client may immediately return a report
            that expresses the progress of the feature selection.

        Returns
        -------
        resp : dict
            Dict containing either the feature selection results or an error report
        """
        first_iter = True
        while wait or first_iter:
            first_iter = False
            resp = requests.get(
                self.service_url+'get_results',
                params={'process_id':process_id},
                headers={'Api-Key':self.api_key}
                )
            resp = resp.json()
            if ('results' in resp) and (resp['results']):
                wait = False
            elif wait:
                time.sleep(0.1)
        # if we have results, re-cast the keys as integers,
        # and re-cast performance metrics as floats
        if ('results' in resp) and (resp['results']):
            all_result_keys = list(resp['results'].keys())
            for k in all_result_keys:
                result = resp['results'].pop(k)
                result['best_f1'] = float(result['best_f1'])
                result['best_precision'] = float(result['best_precision'])
                result['best_accuracy'] = float(result['best_accuracy'])
                result['best_recall'] = float(result['best_recall'])
                resp['results'][int(k)] = result 
        return resp

    def delete_results(self,process_id):
        """Delete results by providing the process_id

        Parameters
        ----------
        process_id : int
            Integer id assigned to the process
            when it was initially launched

        Returns
        -------
        resp : dict
            Dict containing a report of success or failure 
            in deleting the process results
        """
        resp = requests.get(
            self.service_url+'delete_results', 
            params={'process_id':process_id},
            headers={'Api-Key':self.api_key}
            )
        return resp.json()

