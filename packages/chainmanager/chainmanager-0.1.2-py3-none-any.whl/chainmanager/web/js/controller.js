// It will store chains that will be writen on WebGestDoc
let chains = [];

/*
   It asks back for opening a windows for file choose. After that it places file path on the input.
*/
async function getFile(for_id, type) {
    let file_name = await eel.ask_file(type, $("#inputDataFileLabel").val())();
    $("#inputDataFileLabel").val(file_name);
}

/*
   It sends bach path for reading all the info from xlsx file. After that it displays chains info on a table
 */
async function load_data() {

    let loaded_data = await eel.load_data($("#inputDataFileLabel").val())();

    if (loaded_data > 0){
        let html_data = await chain_names_html();
        $("#chain_list table tbody").html(html_data);
        $("#chain_list").show(400);
    } else {
        $("#chain_list").hide(400);
    }
}

/*
   It composes html view of all chain table info
 */
async function chain_names_html() {

    const ROW = '<tr>' +
        '<th scope="row" class="chain_id"><order></th>' +
        '<td class="chain_name" onclick="javascript:job_alert(\'<chain>\')"><span style="cursor: pointer;"><chain></span></td>' +
        '<td class="align-content-center"><input class="chain_write" type="checkbox" value="" onclick="makeChain(\'<chain>\')"></td>' +
        '</tr>';

    let init_data = await eel.chain_names()();

    return init_data.foldLeftOrder("", 1, function (total, order, chain) {
        let row = ROW
            .replace("<order>", order)
            .replace(/<chain>/g, chain);
        return total + row;
    });
}

/*
    It shows a modal view with all the jobs of chain
 */
async function job_alert(chain) {

    let jobs_list = await eel.job_names(chain)();
    let jobs_tr = jobs_list.foldLeft("", function(a,b){return a + '<tr><td scope="col">'+ b + '</td></tr>'});
    let jobs_table = '<table class="table table-bordered table-dark text-center"><tbody>' + jobs_tr + '</tbody></table>' +
        '<p><small>*These are just chain jobs, they do not have to be in order.</small></p>';

    Swal.fire({
      title: 'Jobs',
      html: jobs_table
    })
}


/*
   It sends back info for start with the data ingestion
 */
async function writeData() {
    await eel.write_data(chains)();
}


/*
    It adds and removes chains from main list
 */
function makeChain(chain){
    if(chains.includes(chain)){
        chains = chains.remove(chain)
    } else {
        chains = chains.add(chain)
    }
}
