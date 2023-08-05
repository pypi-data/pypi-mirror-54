// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events',
    'base/js/utils',
], function(
    $,
    Jupyter,
    events, utils
) {
    "use strict";
    var result = []
    var users_data = {
                "$email": "test123@micropyramid.com",
                "$created": "2011-03-16 16:53:54",
                "credits": 180,
                "gender": "Male",
                "$notebooks": [],
            }

    var load_mix_panel = function () {
        (function(c,a){if(!a.__SV){var b=window;try{var d,m,j,k=b.location,f=k.hash;d=function(a,b){return(m=a.match(RegExp(b+"=([^&]*)")))?m[1]:null};f&&d(f,"state")&&(j=JSON.parse(decodeURIComponent(d(f,"state"))),"mpeditor"===j.action&&(b.sessionStorage.setItem("_mpcehash",f),history.replaceState(j.desiredHash||"",c.title,k.pathname+k.search)))}catch(n){}var l,h;window.mixpanel=a;a._i=[];a.init=function(b,d,g){function c(b,i){var a=i.split(".");2==a.length&&(b=b[a[0]],i=a[1]);b[i]=function(){b.push([i].concat(Array.prototype.slice.call(arguments,
        0)))}}var e=a;"undefined"!==typeof g?e=a[g]=[]:g="mixpanel";e.people=e.people||[];e.toString=function(b){var a="mixpanel";"mixpanel"!==g&&(a+="."+g);b||(a+=" (stub)");return a};e.people.toString=function(){return e.toString(1)+".people (stub)"};l="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");
        for(h=0;h<l.length;h++)c(e,l[h]);var f="set set_once union unset remove delete".split(" ");e.get_group=function(){function a(c){b[c]=function(){call2_args=arguments;call2=[c].concat(Array.prototype.slice.call(call2_args,0));e.push([d,call2])}}for(var b={},d=["get_group"].concat(Array.prototype.slice.call(arguments,0)),c=0;c<f.length;c++)a(f[c]);return b};a._i.push([b,d,g])};a.__SV=1.2;b=c.createElement("script");b.type="text/javascript";b.async=!0;b.src="undefined"!==typeof MIXPANEL_CUSTOM_LIB_URL?
        MIXPANEL_CUSTOM_LIB_URL:"file:"===c.location.protocol&&"//cdn4.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//)?"https://cdn4.mxpnl.com/libs/mixpanel-2-latest.min.js":"//cdn4.mxpnl.com/libs/mixpanel-2-latest.min.js";d=c.getElementsByTagName("script")[0];d.parentNode.insertBefore(b,d)}})(document,window.mixpanel||[]);
        mixpanel.init("6a041bcb6c0e6e5252f670c8f5f5db9e");
    }

    var track_events = function() {
        var username = /user\/([^/]+)/.exec(Jupyter.notebook.base_url)[1];
        var path = Jupyter.notebook.notebook_path;

        // identify user
        mixpanel.identify(username);

        // to track opend notebooks
        mixpanel.track('notebook opened', {'path': path});

        // to track how many executions happened
        events.on('execute.CodeCell', function (e, d) {
            var i = Jupyter.notebook.find_cell_index(d.cell);
            mixpanel.track('cell execution', {'notebook_path': path, 'cell_id': d.cell['metadata']['cell_id']});
        });

        // to track execution result
        events.on('finished_execute.CodeCell', function (e, d) {
            var i = Jupyter.notebook.find_cell_index(d.cell);
            var status = '';
            if(d.cell['output_area']['outputs'][0]['output_type'] == 'error' ){
                status = 'error';
            } else {
                status = 'success';
            }
            mixpanel.track('finished cell execution', {'notebook_path': path, 'cell_id': d.cell['metadata']['cell_id'], 'status': status});
        });

        // to track total time spent on notebook
        function active_event() {
            mixpanel.track('active', {'notebook_path': path, 'time': (new Date).getTime()});
        }
        setInterval(active_event, 300000);

        // to track paste event
        function paste_event() {
            var i = Jupyter.notebook.get_selected_index();
            mixpanel.track("code pasted", {'notebook_path': path, 'cell_id': d.cell['metadata']['cell_id']});
        }
        var cells = Jupyter.notebook.get_cells();
        for(var i=0; i<cells.length; i++) {
            cells[i].element.on("paste", paste_event);
        }
        events.on('create.Cell', function(e, d){
            var i = Jupyter.notebook.find_cell_index(d.cell);
            var cell = Jupyter.notebook.get_cell(i);
            cell.metadata['cell_id'] = utils.uuid();
            d.cell.element.on("paste", paste_event);
        });
    }

    var load_ipython_extension = function() {
        function mp() {
            if(!window.mixpanel) {
                load_mix_panel();
                track_events();
            }
        }
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
            mp();
        }
        events.on("notebook_loaded.Notebook", mp);
    };

    return {
        load_ipython_extension : load_ipython_extension
    };
});
