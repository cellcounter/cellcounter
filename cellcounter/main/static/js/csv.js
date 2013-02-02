jQuery.fn.toCSV = function() {
  var data = $(this).first(); //Only one table
  var csvData = [];
  var tmpArr = [];
  var tmpStr = '';
  data.find("tr").each(function() {
      tmpArr = [];
      if($(this).find("th").length) {
          $(this).find("th").each(function() {
            tmpStr = $(this).text().replace(/"/g, '""');
            tmpArr.push('"' + tmpStr + '"');
          });
          csvData.push(tmpArr);
      } else {
          $(this).find("td").each(function() {
            if($(this).text().match(/^-{0,1}\d*\.{0,1}\d+$/)) {
                tmpArr.push(parseFloat($(this).text()));
            } else {
                tmpStr = $(this).text().replace(/"/g, '""');
                tmpArr.push('"' + tmpStr + '"');
            }
          });
          csvData.push(tmpArr.join(','));
      }
  });
  var output = csvData.join('\n');
  return output;
}

