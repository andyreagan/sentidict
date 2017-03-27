requirejs.config({
    paths: {
        d3: "{{ d3_url }}",
        hedotools: "{{ hedotools_url }}"
    }
});
require(['d3','hedotools'], function(d3,hedotools) {
    // window.d3 = d3;
    console.log(d3);
    // window.hedotools = hedotools;
    // this won't show by require because it's not returned in the right way
    console.log(hedotools);
});
