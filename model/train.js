const tf = require('@tensorflow/tfjs');
const FormData = require('form-data');
const fetch = require('node-fetch'); // cần cài: npm install node-fetch@2
const readline = require('readline');

function askYesNo(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(question + ' (y/n): ', (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase() === 'y');
    });
  });
}

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
    const prg = progress_i.slice(10, 40);
    let row = [];

    for(let i=1; i<prg.length; i++){
        let e = prg[i]
        let d_v_0 = prg[i][0].v - prg[i-1][0].v
        let d_v_1 = prg[i][1].v - prg[i-1][1].v
        let d_bc_0 = prg[i][0].bc - prg[i-1][0].bc
        let d_bc_1 = prg[i][1].bc - prg[i-1][1].bc
        row.push(parseInt(e[1].bc) );
        row.push(parseInt(e[1].v) );
        row.push(parseInt(e[0].bc) );
        row.push(parseInt(e[0].v) );
        row.push(parseInt(d_v_0))
        row.push(parseInt(d_v_1))
        row.push(parseInt(d_bc_0))
        row.push(parseInt(d_bc_1))
    }
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


// // Bước 6: Hàm tổng
async function build() {
    const rawData = await getDataFromThuhuyen();
    if (!rawData) return;

    const { xs, ys } = preprocessData(rawData);
    // console.log(xs[0])
    // return;


    const inputTensor = tf.tensor2d(xs);
    const labelTensor = tf.tensor2d(ys);

    const model = tf.sequential();
    model.add(tf.layers.dense({ units: 100, activation: 'sigmoid', inputShape: [xs[0].length] }));
    model.add(tf.layers.dense({ units: 18, activation: 'sigmoid' }));
    model.add(tf.layers.dense({ units: 2, activation: 'sigmoid' }));
    model.add(tf.layers.dense({ units: 1, activation: 'sigmoid' }));

    model.compile({
        optimizer: 'sgd',
        loss: 'binaryCrossentropy',
        metrics: ['accuracy']
    });

    await model.fit(inputTensor, labelTensor, {
        epochs: 100,
        batchSize: 32,
        callbacks: {
            onEpochEnd: (epoch, logs) => {
                console.log(`Epoch ${epoch}: loss = ${logs.loss}, acc = ${logs.acc || logs.accuracy}`);
            }
        }
    });
    
    const confirm = await askYesNo("Bạn có muốn lưu mô hình lên server không?");
    if (confirm) {
      await uploadModel(model);
      console.log("✅ Mô hình đã được lưu.");
    } else {
      console.log("❌ Không lưu mô hình.");
    }
}




build()
