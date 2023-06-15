import great_expectations as gx 

CONTEXT_ROOT_FOLDER = "/mnt/c/Users/Martin/Documents/data_folders/great_expectations"

BASE_DIRECTORY = "/mnt/c/Users/Martin/Documents/data_folders/FolderA"

datasource_name = "folder_A_data"

data_asset_name = "csv_data_asset"

context = gx.get_context(context_root_dir=CONTEXT_ROOT_FOLDER)

my_asset = context.get_datasource(datasource_name).get_asset(data_asset_name)

print(my_asset.batch_request_options)

# datasource = context.sources.add_pandas_filesystem(
#     name=datasource_name, base_directory=BASE_DIRECTORY
# )

# my_data_asset = datasource.add_csv_asset(
#     name="csv_data_asset"
# )





# my_batch_request = my_asset.build_batch_request()

# batches = my_asset.get_batch_list_from_batch_request(my_batch_request)


# for batch in batches:
#     print(batch.batch_spec)