function handleProgress(progress_i) {
    function get_percent(a, b){
        return parseFloat((a/(a+b)).toFixed(5))
    }
    // Lấy một phần dữ liệu từ chỉ số 10 đến 40
    const prg = progress_i.slice(30, 40);
    const row = [];

    for (let i = 0; i < prg.length; i++) {
        const curr = prg[i];

        // Kiểm tra dữ liệu hợp lệ và đảm bảo rằng tất cả các giá trị là số
        if (
            !curr || !isValidData(curr[0]) || !isValidData(curr[1]) 
        ) {
            console.warn(`⚠️ Dữ liệu không hợp lệ tại index ${i}`, curr);
            continue;  // Bỏ qua dữ liệu không hợp lệ và tiếp tục với dữ liệu sau
        }

        row.push(get_percent(curr[0].v, curr[1].v))
        row.push(get_percent(curr[0].bc, curr[1].bc))
    }
    console.log(row)
    return row;
}

// Hàm kiểm tra dữ liệu hợp lệ
function isValidData(data) {
    return data && typeof data.v === 'number' && !isNaN(data.v) && typeof data.bc === 'number' && !isNaN(data.bc);
}

async function predict(progress) {
    let value1 = 0;
    let value2 = 0;
    const inputData = handleProgress(progress);
    const inputTensor = tf.tensor2d([inputData]); 

    for(let model of MODELS){
        const output = model.predict(inputTensor); 
        const value = (await output.data())[0];
        const alpha = 0.035
        if(value > (0.5 +  alpha)){value1+=1}
        if(value < (0.5 - alpha)){value2+=1}
    }
    addMessage(`${value1} ${value2}`, "bot")
    if(value1>value2){
        return [1, value1-value2]
    }
    return [2, value2 - value1]
  }