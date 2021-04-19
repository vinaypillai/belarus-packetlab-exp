# Belarus Experiment
Collects data from DNS and HTTP requests made to a list of blocked domains in Belarus.

## Run
```bash
python3 thread_exp.py <blocked_url_file> [<results_outfile>]
```
Outputs a  JSONL file, where each row is in the format
```json
{
    'site':'example.com',
    'http':{
        'status':200,
        'content':'...'
        'error':null
    },
    'dns':{
        'rcode':0,
        'content':'...'
        'error':null
    },
}
```

#### Arguments
 `blocked_url_file`:  Path to a file of newline separated urls to test
 `results_outfile` (optional): Path for which to write experiment data. Defaults to a timestamped JSONL file
