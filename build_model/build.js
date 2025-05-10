const tf = require('@tensorflow/tfjs');
const FormData = require('form-data');
const fetch = require('node-fetch'); // cần cài: npm install node-fetch@2

async function getDataFromThuhuyen() {
    try {
        const response = await fetch("https://thuhuyen.fun/xg79/get_data.php");

        if (!response.ok) {
            throw new Error(`Lỗi HTTP: ${response.status}`);
        }

        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error("Lỗi kết nối:", error);
        return null;
    }
}
function handleProgress(progress_i) {
    const prg = progress_i.slice(30, 40);
    let row = [];

    prg.forEach((e) => {
        row.push(parseFloat((e[1].bc / e[0].bc).toFixed(2)));
        row.push(parseFloat((e[1].v / e[0].v).toFixed(2)));
    });
    return row;
}
function hasNaN1D(array) {
    return array.some(value => isNaN(value));
}

// Bước 2: Xử lý dữ liệu
function preprocessData(data) {
    const data_parser = data.map((e) => JSON.parse(e.progress));
    let example = handleProgress(data_parser[0])
    // const ys = data.map((e) => (+e.d1 + +e.d2 + +e.d3 > 10 ? [1] : [0]));
    // const xs = data_parser.map((e) => handleProgress(e));
    let xs = []
    let ys = []
    for(let i=0; i< data.length; i++){
        let x = handleProgress(data_parser[i]);
        let y = (+data[i].d1 + +data[i].d2 + +data[i].d3 > 10 ? [1] : [0])
        if(x.length === example.length && !hasNaN1D(x) && !isNaN(y[0])){
            xs.push(x);
            ys.push(y)
        }
    }

    return { xs, ys };
}

// // Bước 3: Đào tạo và lưu mô hình lên server
// async function trainModel(xs, ys) {a
//     const model = tf.sequential();
//     model.add(tf.layers.dense({
//         units: 10,
//         inputShape: [xs[0].length],
//         activation: "relu"
//     }));
//     model.add(tf.layers.dense({ units: 1, activation: "sigmoid" }));

//     model.compile({
//         optimizer: tf.train.adam(),
//         loss: tf.losses.meanSquaredError,
//     });

//     const xs = tf.tensor2d(xs);
//     const ys = tf.tensor2d(ys);

//     await model.fit(xs, ys, {
//         epochs: 500,
//         callbacks: {
//             onEpochEnd: (epoch, logs) => {
//                 if (epoch % 100 === 0) {
//                     console.log(`Epoch ${epoch}: loss = ${logs.loss}`);
//                 }
//             },
//         },
//     });

//     // Gửi model lên server
//     await uploadModel(model);

//     return model;
// }

// // Bước 4: Gửi mô hình lên server thông qua API
async function uploadModel(model) {
    await model.save(tf.io.withSaveHandler(async (modelArtifacts) => {
        const form = new FormData();

        // JSON metadata
        const modelJson = JSON.stringify({
            modelTopology: modelArtifacts.modelTopology,
            format: 'layers-model',
            generatedBy: 'TensorFlow.js',
            convertedBy: null,
            weightsManifest: [{
                paths: ['weights.bin'],
                weights: modelArtifacts.weightSpecs,
            }]
        });

        form.append('model.json', Buffer.from(modelJson), {
            contentType: 'application/json',
            filename: 'model.json'
        });

        // Weights data
        form.append('weights.bin', Buffer.from(modelArtifacts.weightData), {
            contentType: 'application/octet-stream',
            filename: 'weights.bin'
        });
        const response = await fetch('https://thuhuyen.fun/xg79/upload_model.php', {
            method: 'POST',
            headers: form.getHeaders(),
            body: form
        });

        const text = await response.text(); // hoặc response.json() nếu PHP trả về JSON
        console.log("📦 Server response:", response.status, text);

        if (!response.ok) {
            throw new Error("❌ Upload model failed");
        }

        console.log("✅ Model uploaded successfully!");
    }));
}
// // Bước 5: Dự đoán bằng mô hình tải từ server


// async function loadModelFromServer() {
//     model = await tf.loadLayersModel('/models/model.json');
//     console.log("Model loaded from server.");
// }

// async function predict(progress) {
//     if (!model) {
//         await loadModelFromServer();
//     }

//     const inputData = handleProgress(progress);
//     const inputTensor = tf.tensor2d([inputData]);
//     const output = model.predict(inputTensor);
//     const value = (await output.data())[0];
//     return value >= 0.5 ? 1 : 2;
// }

// // Bước 6: Hàm tổng
async function build() {
    const rawData = await getDataFromThuhuyen();
    if (!rawData) return;

    const { xs, ys } = preprocessData(rawData);


    const inputTensor = tf.tensor2d(xs);
    const labelTensor = tf.tensor2d(ys);

    const model = tf.sequential();
    model.add(tf.layers.dense({ units: 100, activation: 'relu', inputShape: [xs[0].length] }));
    model.add(tf.layers.dense({ units: 1, activation: 'sigmoid' }));

    model.compile({
        optimizer: 'sgd',
        loss: 'binaryCrossentropy',
        metrics: ['accuracy']
    });

    await model.fit(inputTensor, labelTensor, {
        epochs: 500,
        batchSize: 32,
        callbacks: {
            onEpochEnd: (epoch, logs) => {
                console.log(`Epoch ${epoch}: loss = ${logs.loss}, acc = ${logs.acc || logs.accuracy}`);
            }
        }
    });
    
    console.log("✅ Training hoàn tất");
    await  uploadModel(model)
}


const model = await tf.loadLayersModel("https://thuhuyen.fun/xg79/get_model.php");
console.log("✅ Model loaded từ server");


// build()
