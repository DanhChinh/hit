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
        row.push(curr[1].bc, curr[1].v, curr[0].bc, curr[0].v, d_v_0, d_v_1, d_bc_0, d_bc_1, curr[1].bc- curr[0].bc, curr[1].v, curr[0].v);
    }

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
        if(value > 0.505){value1+=1}
        if(value < 0.495){value2+=1}
    }
    addMessage(`${value1} ${value2}`, "bot")
    if(value1>value2){
        return [1, value1-value2]
    }
    return [2, value2 - value1]
  }