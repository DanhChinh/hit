function handleProgress(progress_i) {
    const prg = progress_i.slice(30, 40);
    let row = [];

    prg.forEach((e) => {
        row.push(parseFloat((e[1].bc / e[0].bc).toFixed(2)));
        row.push(parseFloat((e[1].v / e[0].v).toFixed(2)));
    });
    return row;
}

async function predict(progress) {
    const inputData = handleProgress(progress);
    const inputTensor = tf.tensor2d([inputData]); // Chuyển đầu vào thành tensor
    const output = model.predict(inputTensor); // Dự đoán đầu ra
    const value = (await output.data())[0]; // Lấy giá trị dự đoán đầu tiên
    console.log(value," <--- ", inputData);
  
    return value >= 0.5 ? 1 : 2;
  }