
window.onload = function() {
	document.getElementById("food").onclick = getQuery;
	document.getElementById("education").onclick = getQuery;
	document.getElementById("shelter").onclick = getQuery;
	document.getElementById("medical").onclick = getQuery;
	document.getElementById("back").onclick = function() {
		document.getElementById("back").style.display = "none";
		document.getElementById("services").style.display = "initial";
		if(document.getElementById("results").style.display === "none") {
			document.getElementById("results").style.display = "block";
			document.getElementById("services").style.display = "none";
			document.getElementById("back").style.display = "initial";
			document.getElementById("facility").innerHTML = "";
		} else {
			document.getElementById("results").innerHTML = "";
		}
	};
	document.getElementById("slider").onchange = range;
	getLocation()
};

function range() {
	var current = parseInt(document.getElementById("slider").value);
	document.getElementById("currentRange").innerHTML = "Range: " + current + " miles";
}



