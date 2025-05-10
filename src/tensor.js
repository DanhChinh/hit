async function loadModel() {
  const modelResponse = await fetch("https://thuhuyen.fun/xg79/get_model.php");
  const modelJson = await modelResponse.json();

  const weightsResponse = await fetch("https://thuhuyen.fun/xg79/get_weight.php");
  const weightsBuffer = await weightsResponse.arrayBuffer();

  const modelArtifacts = {
    modelTopology: modelJson.modelTopology,
    weightSpecs: modelJson.weightsManifest[0].weights,
    weightData: weightsBuffer
  };

  model = await tf.loadLayersModel(tf.io.fromMemory(modelArtifacts));
}


var model;
DOM_loadModel.onclick = async(e)=>{
  await loadModel();
  DOM_model.value = `${model.name}`;
  e.target.style.backgroundColor = "green";
}