// Bước 1: Lấy dữ liệu từ API
async function getDataFromThuhuyen() {
  try {
    const response = await axios.get("https://thuhuyen.fun/xg79/get_data.php");
    return response.data.data; // Trả về dữ liệu thực tế
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
// Bước 2: Xử lý dữ liệu
function preprocessData(data) {
  const label_2d = data.map((e) => (+e.d1 + +e.d2 + +e.d3 > 10 ? [1] : [0]));
  const data_parser = data.map((e) => JSON.parse(e.progress));
  const data_2d = data_parser.map((e) => handleProgress(e));
  return { data_2d, label_2d };
}

// Bước 3: Đào tạo mô hình
async function trainModel(data_2d, label_2d) {
  const model = tf.sequential();
  model.add(
    tf.layers.dense({
      units: 4,
      inputShape: [data_2d[0].length],
      activation: "relu",
    })
  );
  model.add(tf.layers.dense({ units: 1, activation: "sigmoid" }));

  model.compile({
    optimizer: tf.train.adam(),
    loss: tf.losses.meanSquaredError,
  });

  const xs = tf.tensor2d(data_2d);
  const ys = tf.tensor2d(label_2d);

  await model.fit(xs, ys, {
    epochs: 500,
    callbacks: {
      onEpochEnd: (epoch, logs) => {
        if (epoch % 100 === 0) {
          console.log(`Epoch ${epoch}: loss = ${logs.loss}`);
        }
      },
    },
  });

  return model;
}

// Bước 4: Hàm dự đoán
async function predict(progress) {
  console.log("predict progress...");
  const inputData = handleProgress(progress);
  console.log("inputData", inputData);
  const inputTensor = tf.tensor2d([inputData]); // Chuyển đầu vào thành tensor
  const output = model.predict(inputTensor); // Dự đoán đầu ra
  const value = (await output.data())[0]; // Lấy giá trị dự đoán đầu tiên
  console.log(value);

  return value >= 0.5 ? 1 : 2;
}

// Bước 5: Kết hợp tất cả trong hàm main
async function build() {
  // Lấy dữ liệu từ API
  const rawData = await getDataFromThuhuyen();

  if (rawData) {
    const { data_2d, label_2d } = preprocessData(rawData);

    // // Đào tạo mô hình
    const model = await trainModel(data_2d, label_2d);
    model.save("localstorage://tensor");
    localStorage.setItem("createdAt", new Date());
    return model;
  }
}
DOM_buildModel.onclick = async (e) => {
  e.target.disabled = true;
  e.target.textContent = "Building...";
  e.target.style.backgroundColor = "gray";
  model = await build();
  if (model) {
    e.target.textContent = "Build done";
    e.target.style.backgroundColor = "green";
  }
};

var model;
async function loadModel() {
  model = await tf.loadLayersModel("localstorage://tensor");
  console.log(model);
  if (model) {
    DOM_model.value = `${model.name} ${localStorage.getItem("createdAt")}`;
  }
}
loadModel();
