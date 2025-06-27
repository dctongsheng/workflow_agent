from example import auto_fill_parameters_data
def get_data_from_auto_fill_params(data_choose):
    """
    从自动填充参数中获取数据
    """ 
    # data_choose=json.loads(data_choose)
    final_res={}
    res_file_list = []
    res_forder_list = []
    for i in data_choose["records"]:
        print(i["dataType"])
        if i["dataType"]=="0":
            sun_param={}
            for key,value in i.items():
                if key in ["name","omics","menuPath","chipId"] and value != "":
                    
                    sun_param[key]=value
            res_file_list.append(sun_param)
        elif i["dataType"]=="1":
            print(i)
            sun_param={}
            for key,value in i.items():
                if key in ["name","omics","menuPath","chipId"] and value != "":
                    
                    sun_param[key]=value
            res_forder_list.append(sun_param)
    if len(res_file_list)>0:
        final_res["用户选中的文件："]=res_file_list
    if len(res_forder_list)>0:
        final_res["用户选中的文件夹"]=res_forder_list
    return final_res

if __name__ == "__main__":
    data_choose=auto_fill_parameters_data
    res=get_data_from_auto_fill_params(data_choose)
    print(res)