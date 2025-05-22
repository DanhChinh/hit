const tf = require('@tensorflow/tfjs');
const FormData = require('form-data');
const fetch = require('node-fetch'); // npm install node-fetch@2
const readline = require('readline');

// ------------------- Hàm phụ trợ -------------------
function askYesNo(question) {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    return new Promise(resolve => {
        rl.question(question + ' (y/n): ', (answer) => {
            rl.close();
            resolve(answer.trim().toLowerCase() === 'y');
        });
    });
}

function hasNaN1D(array) {
    return array.some(value => isNaN(value));
}

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function split2DArray(array2D, numChunks) {
    const rowsPerChunk = Math.floor(array2D.length / numChunks);
    const result = [];
    for (let i = 0; i < numChunks; i++) {
        const start = i * rowsPerChunk;
        const end = i === numChunks - 1 ? array2D.length : start + rowsPerChunk;
        result.push(array2D.slice(start, end));
    }
    return result;
}

// ------------------- Lấy & xử lý dữ liệu -------------------
async function getDataFromThuhuyen() {
    try {
        const response = await fetch('https://thuhuyen.fun/xg79/get_data.php');
        if (!response.ok) throw new Error(`Lỗi HTTP: ${response.status}`);
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error("Lỗi kết nối:", error);
        return null;
    }
}

function ghiFile(arr, filename){
        const fs = require('fs');
    const data = arr.map(row => row.join(',')).join('\n');
    // Ghi vào file
    fs.writeFile(filename, data, (err) => {
      if (err) throw err;
      console.log('Đã ghi mảng 2 chiều thành từng dòng!');
    });
}
function handleProgress(progress_i) {
    // Lấy một phần dữ liệu từ chỉ số 10 đến 40
    const prg = progress_i.slice(10, 40);
    const row = [];

    for (let i = 1; i < prg.length; i++) {
        const curr = prg[i];
        const prev = prg[i - 1];

        // Kiểm tra dữ liệu hợp lệ và đảm bảo rằng tất cả các giá trị là số
        if (
            !curr || !prev || 
            !isValidData(curr[0]) || !isValidData(curr[1]) || 
            !isValidData(prev[0]) || !isValidData(prev[1])
        ) {
            console.warn(`⚠️ Dữ liệu không hợp lệ tại index ${i}`, curr);
            continue;  // Bỏ qua dữ liệu không hợp lệ và tiếp tục với dữ liệu sau
        }

        // Tính toán sự khác biệt giữa các giá trị
        const d_v_0 = curr[0].v - prev[0].v;
        const d_v_1 = curr[1].v - prev[1].v;
        const d_bc_0 = curr[0].bc - prev[0].bc;
        const d_bc_1 = curr[1].bc - prev[1].bc;

        // Thêm kết quả vào mảng row
        row.push(curr[1].bc, curr[1].v, curr[0].bc, curr[0].v, d_v_0, d_v_1, d_bc_0, d_bc_1);
    }

    return row;
}

// Hàm kiểm tra dữ liệu hợp lệ
function isValidData(data) {
    return data && typeof data.v === 'number' && !isNaN(data.v) && typeof data.bc === 'number' && !isNaN(data.bc);
}

function quaNuaLaKhong(arr) {
    let demKhong = arr.filter(x => x == 0).length;
    return demKhong > arr.length / 2;
  }
  
function preprocessData(data) {
    const dataParser = data.map(e => JSON.parse(e.progress));
    const example = handleProgress(dataParser[0]);

    const xs = [];
    const ys = [];

    for (let i = 0; i < data.length; i++) {
        const x = handleProgress(dataParser[i]);
        const y = +data[i].d1 + +data[i].d2 + +data[i].d3 > 10 ? [1] : [0];
        if(quaNuaLaKhong(x)){
            console.warn(`❌ Dữ liệu không hợp lệ 0000 tại mẫu ${data[i].sid}`);
        }
        if (x && x.length === example.length && !hasNaN1D(x) && !isNaN(y[0])) {
            xs.push(x);
            ys.push(y);
        }
         else {
            console.warn(`❌ Dữ liệu không hợp lệ tại mẫu ${data[i].sid}`);
        }
    }

    return { xs, ys };
}

// ------------------- Upload model -------------------
async function uploadModel(model, index) {
    await model.save(tf.io.withSaveHandler(async (modelArtifacts) => {
        const form = new FormData();

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

        form.append(`model${index}.json`, Buffer.from(modelJson), {
            contentType: 'application/json',
            filename: `model${index}.json`
        });

        form.append(`weights${index}.bin`, Buffer.from(modelArtifacts.weightData), {
            contentType: 'application/octet-stream',
            filename: `weights${index}.bin`
        });

        const response = await fetch('https://thuhuyen.fun/xg79/upload_model.php', {
            method: 'POST',
            headers: form.getHeaders(),
            body: form
        });

        const text = await response.text();
        console.log(`📦 Server response [model ${index}]:`, response.status, text);
        if (!response.ok) throw new Error("❌ Upload model failed");
    }));
}

// ------------------- Hàm chính -------------------
async function build() {
    const rawData = await getDataFromThuhuyen();
    if (!rawData) {
        console.error('❌ Không có dữ liệu.');
        return;
    }

    let { xs, ys } = preprocessData(rawData);
   
    // Chia dữ liệu thành các phần nhỏ
    const xss = split2DArray(xs, 10);
    const yss = split2DArray(ys, 10);
    

    // Khởi tạo mô hình một lần duy nhất
    const model = tf.sequential();
    model.add(tf.layers.dense({
        units: 128, 
        activation: 'relu', 
        inputShape: [xs[0].length]
    }));
    
    // Thêm lớp Batch Normalization để ổn định huấn luyện
    model.add(tf.layers.batchNormalization());
    
    // Lớp thứ hai
    model.add(tf.layers.dense({
        units: 128, 
        activation: 'relu'
    }));
    
    // Thêm lớp Dropout để giảm overfitting
    model.add(tf.layers.dropout(0.2)); // 20% dropout
    
    // Lớp output, có thể là sigmoid hoặc softmax tùy vào loại bài toán
    model.add(tf.layers.dense({
        units: 1,  // Cho bài toán phân loại nhị phân
        activation: 'sigmoid' // Nếu là phân loại nhị phân
    }));
    
    // Biên dịch mô hình chỉ một lần
    model.compile({
        optimizer: 'adam',  // Adam thường hoạt động tốt hơn so với SGD trong hầu hết các trường hợp
        loss: 'binaryCrossentropy',
        metrics: ['accuracy']
    });

    // Lặp qua từng phần dữ liệu và huấn luyện mô hình
    for (let i = 0; i < 10; i++) {
        let chunkXs = xss[i];
        let chunkYs = yss[i];

        // Kiểm tra dữ liệu trước khi tạo tensor
        if (!Array.isArray(chunkXs) || chunkXs.length === 0 || !Array.isArray(chunkXs[0])) {
            console.error(`❌ chunkXs không hợp lệ tại model ${i}`);
            continue;
        }
        if (!Array.isArray(chunkYs) || chunkYs.length === 0 || !Array.isArray(chunkYs[0])) {
            console.error(`❌ chunkYs không hợp lệ tại model ${i}`);
            continue;
        }

        // Tạo Tensor từ chunk dữ liệu
        const inputTensor = tf.tensor2d(chunkXs);
        const labelTensor = tf.tensor2d(chunkYs);

        // Huấn luyện mô hình với mỗi batch dữ liệu
        await model.fit(inputTensor, labelTensor, {
            epochs: 50,  // Giảm số epoch xuống để tránh overfitting, bạn có thể thử điều chỉnh
            batchSize: randomInt(10, 100),  // Giữ batchSize ngẫu nhiên
            validationSplit: 0.2,  // Dùng 20% dữ liệu để xác nhận
            callbacks: {
                onEpochEnd: (epoch, logs) => {
                    console.log(`Epoch ${epoch}: loss = ${logs.loss}, acc = ${logs.acc || logs.accuracy}`);
                }
            }
        });

        // Sau khi huấn luyện xong cho một chunk, lưu mô hình (nếu cần)
        if (true) {  // Bạn có thể thay đổi điều kiện này theo nhu cầu
            await uploadModel(model, i);
            console.log(`✅ Mô hình ${i} đã được lưu.`);
        } else {
            console.log(`❌ Không lưu mô hình ${i}.`);
        }
    }
}

// ------------------- Chạy -------------------
build();
