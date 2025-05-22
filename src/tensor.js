// async function loadModel() {
//   const modelResponse = await fetch("https://thuhuyen.fun/xg79/get_model.php");
//   const modelJson = await modelResponse.json();

//   const weightsResponse = await fetch("https://thuhuyen.fun/xg79/get_weight.php");
//   const weightsBuffer = await weightsResponse.arrayBuffer();

//   const modelArtifacts = {
//     modelTopology: modelJson.modelTopology,
//     weightSpecs: modelJson.weightsManifest[0].weights,
//     weightData: weightsBuffer
//   };

//   model = await tf.loadLayersModel(tf.io.fromMemory(modelArtifacts));
// }
// Hàm tải mô hình và trọng số từ API PHP
// Hàm tải mô hình và trọng số từ API PHP
async function loadAllModels() {
  try {
      const response = await fetch('https://thuhuyen.fun/xg79/get_model.php');
      const models = await response.json();
      console.log(models);

      if (models.error) {
          console.error(models.error);
          return;
      }

      for (const modelData of models) {
          const modelJson = JSON.parse(modelData.model); // Cấu trúc mô hình JSON
          const weightsBin = Uint8Array.from(atob(modelData.weights), c => c.charCodeAt(0)); // Chuyển đổi base64 thành ArrayBuffer

          // Tạo artifacts cho mô hình (bao gồm cấu trúc mô hình và trọng số)
          const modelArtifacts = {
              modelTopology: modelJson.modelTopology,  // Cấu trúc mô hình JSON
              weightSpecs: modelJson.weightsManifest[0].weights,  // Thông tin về các trọng số
              weightData: weightsBin,  // Trọng số (dưới dạng ArrayBuffer)
          };

          // Tạo mô hình từ artifacts đã được chuẩn bị
          const model = await tf.loadLayersModel(tf.io.fromMemory(modelArtifacts));
          MODELS.push(model)
          
          addMessage(`Model ${modelData.model_id} loaded successfully!`, "server");
      }
      console.log(MODELS)

  } catch (error) {
      console.error('Error loading models:', error);
  }
}




var MODELS = [];
DOM_loadModel.onclick = async(e)=>{
  loadAllModels();
  // DOM_model.value = `${model.name}`;
  e.target.style.backgroundColor = "green";
}