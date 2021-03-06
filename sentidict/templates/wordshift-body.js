var lens = [{{ lens }}];
var words = [{{ words }}];
var refF = [{{ refF }}];
var compF = [{{ compF }}];

var my_shifter =  hedotools.shifter();
my_shifter._refF(refF);
my_shifter._compF(compF);
my_shifter._lens(lens);
my_shifter._words(words);

// my_shifter.plotdist(true);

// do the shifting
{% if selfshift %}
my_shifter.selfShifter();
{% else %}
my_shifter.shifter();
{% endif %}

my_shifter.setWidth(400);
// my_shifter.setHeight(800);

// don't use the default title
// set own title
// but leave all of the default sizes and labels

// extract these:
var compH = my_shifter._compH();
var refH = my_shifter._refH();
// from the code inside the shifter:
if (compH >= refH) {
    var happysad = "happier";
}
else { 
    var happysad = "less happy";
}

// also from inside the shifter:
// var comparisonText = splitstring(["Reference happiness: "+refH.toFixed(2),"Comparison happiness: "+compH.toFixed(2),"Why comparison is "+happysad+" than reference:"],boxwidth-10-logowidth,'14px arial');
// our adaptation:
var comparisonText = ["{{ title }}","","{{ ref_name_happs }} happiness: "+refH.toFixed(2),"{{ comp_name_happs }} happiness: "+compH.toFixed(2),"Why {{ comp_name }}{{ isare }}"+happysad+" than {{ ref_name }}:"];
// set it:
my_shifter.setText(comparisonText);
my_shifter.setTextBold(0);
my_shifter.setBgcolor("{{ bgcolor }}");
my_shifter.setTopTextSizes([24,16,16,16,16]);
my_shifter.setTextColors(["#D8D8D8","#D8D8D8","#D8D8D8","#D8D8D8","#D8D8D8",]);
my_shifter.setFontSizes([16,10,22,11,8,8,13]);
// [bigshifttextsize,xaxisfontsize,xylabelfontsize,wordfontsize,distlabeltext,creditfontsize,resetfontsize];

my_shifter.setfigure(d3.select('#figure{{ divnum }}'));
my_shifter.plot();

d3.selectAll('g.resetbutton').remove();
d3.selectAll('.credit').remove();
