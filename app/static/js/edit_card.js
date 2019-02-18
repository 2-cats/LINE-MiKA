window.onload = function (e) {
    industryName = document.getElementById("industry_name").value
    setIndustryValue(industryName)
};

function setIndustryValue(industryName){
    var sel = document.getElementById('industry');
    for(var i = 0, j = sel.options.length; i < j; ++i) {
        if(sel.options[i].innerHTML === industryName) {
           sel.selectedIndex = i;
           break;
        }
    }
}