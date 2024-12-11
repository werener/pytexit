function preprocess(string) {
	let processedString = "";
	let parCount = 0;

	function nextChar(i) {
		for (let j = i + 1; j < string.length; j++) {
			if (string[j] != " " && string[j]) {
				return {
					value: string[j],
					index: j,
				};
			}
		}
		return {
			value: undefined,
			index: string.length - 1,
		};
	}

	function prevChar(i) {
		for (let j = i - 1; j > 0; j--) {
			if (string[j] != " ") {
				return {
					value: string[j],
					index: j,
				};
			}
		}
		return {
			value: undefined,
			index: 0,
		};
	}

	for (let i = 0; i < string.length; i++) {
		switch (string[i]) {
			case " ":
				break;
			case "(":
				parCount++;
				processedString += "(";
				break;
			case ")":
				parCount--;
				processedString += ")";
				break;
			case "[":
				parCount++;
				processedString += "(";
				break;
			case "]":
				parCount--;
				processedString += ")";
				break;
			case "{":
				parCount++;
				processedString += "(";
				break;
			case "}":
				parCount--;
				processedString += ")";
				break;
			case "^":
				processedString += "**";
				break;
			case ":":
				processedString += "/";
				break;
			case "!":
				if (
					nextChar(i).value == "=" &&
					nextChar(nextChar(i).index).value == "="
				) {
					processedString += "*fact()==";
					i = nextChar(nextChar(i).index).index;
				} else if (string[i + 1] == "=") {
					processedString += "!=";
					i++;
				} else processedString += "*fact()";

				break;

			case "=":
				if (nextChar(i).value != "=" && prevChar(i).value != "=") {
					processedString += "==";
					i++;
				}
			default:
				processedString += string[i];
		}
	}

	if (parCount > 0) {
		processedString += ")".repeat(parCount);
	} else if (parCount < 0) {
		processedString = "(".repeat(-parCount) + processedString;
	}
	return processedString;
}



let latexVariable = "";
const input = document.getElementById("input");
const latexOutput = document.getElementById("output");

input.addEventListener("input", async () => {
    console.log(typeof input.value)
	let preprocessedString = preprocess(input.value);
    console.log(encodeURIComponent(preprocessedString))
	let latexJson = await fetch(`latex?input=${encodeURIComponent(preprocessedString)}`, {
		headers: {
			Accept: "application/json",
			"Content-Type": "application/json",
		},
	}).then((r) => r.json());
    console.log(latexJson, latexJson.result)
	if (latexJson.error) {
		return;
	}


	output = document.getElementById("output");
	output.innerHTML = "";
	MathJax.texReset();
	let options = MathJax.getMetricsFor(output);
	MathJax.tex2chtmlPromise(latexJson.result, options).then((node) => {
		output.appendChild(node);
		MathJax.startup.document.clear();
		MathJax.startup.document.updateDocument();
	});
});
