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
async function predict(progress) {
    const inputData = handleProgress(progress);
    const inputTensor = tf.tensor2d([inputData]); 
    const output = model.predict(inputTensor); 
    const value = (await output.data())[0];
    // addMessage(inputData, "bot")
    addMessage(value, "bot")
  
    return value >= 0.5 ? 1 : 2;
  }