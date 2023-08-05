check_and_import <- function(packages){
  tryCatch({
      for(package in packages){
        if(!require(package, character.only = TRUE)){
          library(package, character.only = TRUE)
        }
      }
    }, error = function(e) {
    stop(sprintf("Initialize R script execution environment failed. Reason: %s.", toString(e)))
  })
}

convert_to_list <- function(results){
  result_class = class(results)
  if (result_class == "list"){
    return(results)
  } else {
    return(list(dataset1=results))
  }
}


load_dataframe_from_parquet <- function(parquet_path){
  if(file.exists(parquet_path)){
    r_dataframe <- pd$read_parquet(parquet_path, "pyarrow")
  } else {
    r_dataframe <- NULL
  }

  return(r_dataframe)
}

save_dataframe_to_parquet <- function(r_dataframe, parquet_path){
  class_str = class(r_dataframe)
  if (is.data.frame(r_dataframe) || any(grepl("pandas.core.frame.DataFrame", class_str))) {
    py_dataframe <- r_to_py(r_dataframe)
    py_dataframe$to_parquet(parquet_path, "pyarrow")
  } else if (is.null(r_dataframe)) {
    warning(sprintf("Skip output: '%s' since it's NULL.", parquet_path))
  } else {
    stop(sprintf("Unsupported return type, expect: 'data.frame' or 'pandas.core.frame.DataFrame', actual: '%s'", class_str))
  }
}

print("R script run.")

args = commandArgs(trailingOnly=TRUE)
if (length(args) < 2) {
  stop(sprintf("Invalid arguments count, expect: 2, actual: %d.", length(args)))
}

status_file <- args[2]
error_msg <- ''
tryCatch(withCallingHandlers({
    print("Import packages.")
    check_and_import(list("reticulate", "jsonlite"))

    pd <- import("pandas")
    pa <- import("pyarrow")

    decoded_params <- URLdecode(args[1])
    params <- fromJSON(decoded_params)
    input_paths <- params$input_paths
    output_paths <- params$output_paths
    custom_script <- params$custom_script

    print("R read input parquet file.")
    input_dataframe_1 <- load_dataframe_from_parquet(input_paths[1])
    input_dataframe_2 <- load_dataframe_from_parquet(input_paths[2])

    source(custom_script)
    results <- azureml_main(input_dataframe_1, input_dataframe_2)
    if (!is.null(results)) {
      results <- convert_to_list(results)
      output_dataframe_1 <- results$dataset1
      output_dataframe_2 <- results$dataset2

      print("R generate output parquet file.")
      save_dataframe_to_parquet(output_dataframe_1, output_paths[1])
      save_dataframe_to_parquet(output_dataframe_2, output_paths[2])
    } else {
      warning("Empty result received from custom script.")
    }
  }, error = function(e) {
    error_msg <<- paste(toString(e), toString(sys.calls()), sep="\n")
    stop(e)
  }
), finally = {
  write(error_msg, status_file)
})

print("R script exit.")