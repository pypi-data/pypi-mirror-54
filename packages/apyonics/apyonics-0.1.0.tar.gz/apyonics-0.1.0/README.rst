apyonics
--------

Python client for AIONICS APIs

usage instructions
==================

**import the package**::

    import apyonics

**start a client**::

    client = apyonics.Client(service_url="https://your.service.url",api_key="your-api-key")

**fetch a dataset**::

    # the dataset is returned in a pandas.DataFrame:
    ds = client.get_dataset(dataset_id=0)

**get descriptors by MPID, by dataset and sample id, or by computing directly from POSCAR data**::

    # descriptors are returned in a dict:
    desc_mp1153 = client.get_descriptors_by_mpid('mp-1153')
    desc_li2ge7o15 = client.get_descriptors_from_sample(dataset_id=0,sample_id='Li2Ge7O15')
    desc_poscar = client.compute_poscar_descriptors(<path-to-poscar-file>)

**extend a dataset to include new samples**::

    # the sample is constructed by combining descriptors with experimental data
    sample1 = desc_mp1153.copy()
    sample1['log10_conductivity'] = -7.5
    sample1['superionic_flag'] = False
    new_ds = apyonics.add_to_dataset(ds,sample1)

    # save dataset to local machine as csv:
    apyonics.save_dataset(new_ds,<path-to-new-dataset.csv>)

**upload a dataset to the server (note: not required for modeling!)**::

    # provide the path to the file containing the dataset on your local machine:
    resp = client.upload_dataset(<path-to-new-dataset.csv>)
    new_dsid = resp['dataset_id']

**perform combinatoric selection by dataset id or directly from a local dataset**::

    # run combinatoric selection on saved dataset with dataset_id=0:
    resp = client.run_logreg_combo_selection(0,min_feats=2,max_feats=5,
                                            input_keys=['LLB','SBI','AFC','LASD','LLSD'],
                                            output_key='superionic_flag',penalty='none')

    # (or) run combinatoric selection on locally saved dataset:
    resp = client.run_logreg_combo_selection(<path-to-new-dataset.csv>,min_feats=2,max_feats=5,
                                            input_keys=['LLB','SBI','AFC','LASD','LLSD'],
                                            output_key='superionic_flag',penalty='none')
    process_id = resp['process_id']

    # wait for and collect feature selection results:
    resp2 = client.get_logreg_combo_results(process_id,wait=True)

    # get a plot of best-selected performance metrics with respect to number of descriptors:
    apyonics.plot_logreg_cfs(resp2['results'],show=True)

    # take the best 5 descriptors based on f1 score:
    best_feats = resp2['results'][5]['best_f1_descriptors']

**train a model by dataset id or directly from a locally saved dataset**::

    # train logistic regression from dataset 0:
    resp1 = client.train_logistic_regression(0,input_keys=best_feats,output_key='superionic_flag',penalty='none')

    # (or) train logistic regression on a locally saved dataset:
    resp2 = client.train_logistic_regression(<path-to-new-dataset.csv>,input_keys=best_feats,output_key='superionic_flag',penalty='none')
    new_model_id = resp1['model_id']

**apply a model by MPID, by dataset and sample id, or directly on POSCAR data**::

    # apply the model to descriptors that were already looked up or computed: 
    result1 = client.apply_model(new_model_id,desc_mp1153)
    result2 = client.apply_model(new_model_id,desc_li2ge7o15)
    result3 = client.apply_model(new_model_id,desc_poscar)

    # apply the model by MPID:
    result4 = client.apply_model_to_mpid(new_model_id,'mp-1153')

    # apply the model to a sample from a saved dataset:
    result5 = client.apply_model_to_sample(new_model_id,0,'Li2Ge7O15')

    # apply the model directly to POSCAR data:
    result6 = client.apply_model_to_poscar(new_model_id,<path-to-POSCAR-file>)

**delete a dataset, model, or combinatoric selection result**::

    # delete dataset
    resp = client.delete_dataset(new_dsid)

    # delete model
    resp = client.delete_model(new_model_id)

    # delete results
    resp = client.delete_results(process_id)

