`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: USTC ESLAB锛圗mbeded System Lab锛?
// Engineer: Haojun Xia(xhjustc@mail.ustc.edu.cn)
// Create Date: 2019/02/08 16:29:41
// Design Name: RISCV-Pipline CPU
// Module Name: RV32Core
// Target Devices: Nexys4
// Tool Versions: Vivado 2017.4.1
// Description: Top level of our CPU Core
//////////////////////////////////////////////////////////////////////////////////
module RV32Core(
    input wire CPU_CLK,
    input wire CPU_RST,
    input wire [31:0] CPU_Debug_DataRAM_A2,
    input wire [31:0] CPU_Debug_DataRAM_WD2,
    input wire [3:0] CPU_Debug_DataRAM_WE2,
    output wire [31:0] CPU_Debug_DataRAM_RD2,
    input wire [31:0] CPU_Debug_InstRAM_A2,
    input wire [31:0] CPU_Debug_InstRAM_WD2,
    input wire [ 3:0] CPU_Debug_InstRAM_WE2,
    output wire [31:0] CPU_Debug_InstRAM_RD2
    );
	//wire values definitions
    wire StallF, FlushF, StallD, FlushD, StallE, FlushE, StallM, FlushM, StallW, FlushW;
    wire [31:0] PC_In;
    wire [31:0] PCF;
    wire [31:0] Instr, PCD;
    wire JalD, JalrD, LoadNpcD, MemToRegD, AluSrc1D;
    wire [2:0] RegWriteD;
    wire [3:0] MemWriteD;
    wire [1:0] RegReadD;
    wire [2:0] BranchTypeD;
    wire [4:0] AluContrlD;
    wire [1:0] AluSrc2D;
    wire [2:0] RegWriteW;
    wire [4:0] RdW;
    wire [31:0] RegWriteData;
    wire [31:0] DM_RD_Ext;
    wire [2:0] ImmType;
    wire [31:0] ImmD;
    wire [31:0] JalNPC;
    wire [31:0] BrNPC; 
    wire [31:0] ImmE;
    wire [6:0] OpCodeD, Funct7D;
    wire [2:0] Funct3D;
    wire [4:0] Rs1D, Rs2D, RdD;
    wire [4:0] Rs1E, Rs2E, RdE;
    wire [31:0] RegOut1D;
    wire [31:0] RegOut1E;
    wire [31:0] RegOut2D;
    wire [31:0] RegOut2E;
    wire JalrE;
    wire [2:0] RegWriteE;
    wire MemToRegE;
    wire [3:0] MemWriteE;
    wire LoadNpcE;
    wire [1:0] RegReadE;
    wire [2:0] BranchTypeE;
    wire [3:0] AluContrlE;
    wire AluSrc1E;
    wire [1:0] AluSrc2E;
    wire [31:0] Operand1;
    wire [31:0] Operand2;
    wire BranchE;
    wire [31:0] AluOutE;
    wire [31:0] AluOutM; 
    wire [31:0] ForwardData1;
    wire [31:0] ForwardData2;
    wire [31:0] PCE;
    wire [31:0] StoreDataM; 
    wire [4:0] RdM;
    wire [31:0] PCM;
    wire [2:0] RegWriteM;
    wire MemToRegM;
    wire [3:0] MemWriteM;
    wire LoadNpcM;
    wire [31:0] DM_RD;
    wire [31:0] ResultM;
    wire [31:0] ResultW;
    wire MemToRegW;
    wire [1:0] Forward1E;
    wire [1:0] Forward2E;
    wire [1:0] LoadedBytesSelect;
	//for BTB
	wire BranchPredictedF; //BTB命中，表示可以进行预测
	wire BranchPredictedD;
	wire BranchPredictedE;
	wire [31:0] BranchPredictedPCF;
	//for BHT
	wire BranchPredictedTakenF; //BHT命中，表示预测跳转
	wire BranchPredictedTakenD;
	wire BranchPredictedTakenE;
	//count
	reg [31:0] all_instr_count;
	reg [31:0] branch_instr_count;
	reg [31:0] right_predict_count;
	reg [31:0] error_predict_count;
    //wire values assignments
    assign {Funct7D, Rs2D, Rs1D, Funct3D, RdD, OpCodeD} = Instr;
    assign JalNPC=ImmD+PCD;
    assign ForwardData1 = Forward1E[1]?(AluOutM):( Forward1E[0]?RegWriteData:RegOut1E );
    assign Operand1 = AluSrc1E?PCE:ForwardData1;
    assign ForwardData2 = Forward2E[1]?(AluOutM):( Forward2E[0]?RegWriteData:RegOut2E );
    assign Operand2 = AluSrc2E[1]?(ImmE):( AluSrc2E[0]?Rs2E:ForwardData2 );
    assign ResultM = LoadNpcM ? (PCM+4) : AluOutM;
    assign RegWriteData = ~MemToRegW?ResultW:DM_RD_Ext;

	// ---------------------------------------------
	// Count
	// ---------------------------------------------
	
	always @ (posedge CPU_CLK or posedge CPU_RST) begin 
		if(CPU_RST) begin
			all_instr_count <= 0;
			branch_instr_count <= 0;
			right_predict_count <= 0;
			error_predict_count <= 0;
		end else begin
			if(FlushE && FlushD)
				all_instr_count <= all_instr_count - 1;
			else if(FlushE || FlushD)
				all_instr_count <= all_instr_count;
			else
				all_instr_count <= all_instr_count + 1;
			if(BranchTypeE != 3'b000) begin
				branch_instr_count <= branch_instr_count + 1;
				if((BranchPredictedE && (BranchPredictedTakenE ^ BranchE)) || (~BranchPredictedE && BranchE))
					error_predict_count <= error_predict_count + 1;
				else 
					right_predict_count <= right_predict_count + 1;
			end
		end
	end
	
    //Module connections
    // ---------------------------------------------
    // PC-IF
    // ---------------------------------------------
    NPC_Generator NPC_Generator1(
        .PCF(PCF),
		.PCE(PCE),
        .JalrTarget(AluOutE), 
        .BranchTarget(BrNPC), 
        .JalTarget(JalNPC),
		.BranchPredictedF(BranchPredictedF), //for BTB
		.BranchPredictedTargetF(BranchPredictedPCF), //for BTB
		.BranchPredictedE(BranchPredictedE), //for BTB
		.BranchPredictedTakenF(BranchPredictedTakenF), //for BHT
		.BranchPredictedTakenE(BranchPredictedTakenE), //for BHT
        .BranchE(BranchE),
        .JalD(JalD),
        .JalrE(JalrE),
        .PC_In(PC_In)
    );

    IFSegReg IFSegReg1(
        .clk(CPU_CLK),
        .en(~StallF),
        .clear(FlushF), 
        .PC_In(PC_In),
        .PCF(PCF)
    );

	//BTB
	BTB BTB1(
		.clk(~CPU_CLK),
		.rst(CPU_RST),
		.rd_PC(PCF), //输入当前PC
		.rd_predicted_PC(BranchPredictedPCF), //输出预测的下一个PC
		.rd_predicted(BranchPredictedF), //是否可以预测的标志
		.wr_req(BranchE), //实际有跳转就更新BTB
		.wr_PC(PCE), //wr_req为1才使用
		.wr_predicted_PC(BrNPC) //wr_req为1才使用
	);

	
	//BHT
	BHT BHT1(
		.clk(~CPU_CLK),
		.rst(CPU_RST),
		.rd_PC(PCF), //输入当前PC
		.rd_predicted_taken(BranchPredictedTakenF), //预测是否跳转的标志
		.wr_req(BranchTypeE != 3'b000), //是branch指令就要更新BHT，无论是否实际跳转
		.wr_PC(PCE), //wr_req为1才使用
		.wr_taken(BranchE) //wr_PC是否实际跳转，wr_req为1才使用
	);

    // ---------------------------------------------
    // ID stage
    // ---------------------------------------------
    IDSegReg IDSegReg1(
        .clk(CPU_CLK),
        .clear(FlushD),
        .en(~StallD),
        .A(PCF),
        .RD(Instr),
        .A2(CPU_Debug_InstRAM_A2),
        .WD2(CPU_Debug_InstRAM_WD2),
        .WE2(CPU_Debug_InstRAM_WE2),
        .RD2(CPU_Debug_InstRAM_RD2),
        .PCF(PCF),
        .PCD(PCD),
		.BranchPredictedF(BranchPredictedF), //for BTB
		.BranchPredictedD(BranchPredictedD), //for BTB
		.BranchPredictedTakenF(BranchPredictedTakenF), //for BHT
		.BranchPredictedTakenD(BranchPredictedTakenD)  //for BHT
    );

    ControlUnit ControlUnit1(
        .Op(OpCodeD),
        .Fn3(Funct3D),
        .Fn7(Funct7D),
        .JalD(JalD),
        .JalrD(JalrD),
        .RegWriteD(RegWriteD),
        .MemToRegD(MemToRegD),
        .MemWriteD(MemWriteD),
        .LoadNpcD(LoadNpcD),
        .RegReadD(RegReadD),
        .BranchTypeD(BranchTypeD),
        .AluContrlD(AluContrlD),
        .AluSrc1D(AluSrc1D),
        .AluSrc2D(AluSrc2D),
        .ImmType(ImmType)
    );

    ImmOperandUnit ImmOperandUnit1(
        .In(Instr[31:7]),
        .Type(ImmType),
        .Out(ImmD)
    );

    RegisterFile RegisterFile1(
        .clk(CPU_CLK),
        .rst(CPU_RST),
        .WE3(|RegWriteW),
        .A1(Rs1D),
        .A2(Rs2D),
        .A3(RdW),
        .WD3(RegWriteData),
        .RD1(RegOut1D),
        .RD2(RegOut2D)
    );

    // ---------------------------------------------
    // EX stage
    // ---------------------------------------------
    EXSegReg EXSegReg1(
        .clk(CPU_CLK),
        .en(~StallE),
        .clear(FlushE),
        .PCD(PCD),
        .PCE(PCE), 
        .JalNPC(JalNPC),
        .BrNPC(BrNPC), 
        .ImmD(ImmD),
        .ImmE(ImmE),
        .RdD(RdD),
        .RdE(RdE),
        .Rs1D(Rs1D),
        .Rs1E(Rs1E),
        .Rs2D(Rs2D),
        .Rs2E(Rs2E),
        .RegOut1D(RegOut1D),
        .RegOut1E(RegOut1E),
        .RegOut2D(RegOut2D),
        .RegOut2E(RegOut2E),
        .JalrD(JalrD),
        .JalrE(JalrE),
        .RegWriteD(RegWriteD),
        .RegWriteE(RegWriteE),
        .MemToRegD(MemToRegD),
        .MemToRegE(MemToRegE),
        .MemWriteD(MemWriteD),
        .MemWriteE(MemWriteE),
        .LoadNpcD(LoadNpcD),
        .LoadNpcE(LoadNpcE),
        .RegReadD(RegReadD),
        .RegReadE(RegReadE),
        .BranchTypeD(BranchTypeD),
        .BranchTypeE(BranchTypeE),
        .AluContrlD(AluContrlD),
        .AluContrlE(AluContrlE),
        .AluSrc1D(AluSrc1D),
        .AluSrc1E(AluSrc1E),
        .AluSrc2D(AluSrc2D),
        .AluSrc2E(AluSrc2E),
		.BranchPredictedD(BranchPredictedD), //for BTB
		.BranchPredictedE(BranchPredictedE), //for BTB
		.BranchPredictedTakenD(BranchPredictedTakenD), //for BHT
		.BranchPredictedTakenE(BranchPredictedTakenE)  //for BHT
    	); 

    ALU ALU1(
        .Operand1(Operand1),
        .Operand2(Operand2),
        .AluContrl(AluContrlE),
        .AluOut(AluOutE)
    	);

    BranchDecisionMaking BranchDecisionMaking1(
        .BranchTypeE(BranchTypeE),
        .Operand1(Operand1),
        .Operand2(Operand2),
        .BranchE(BranchE)
        );

    // ---------------------------------------------
    // MEM stage
    // ---------------------------------------------
    MEMSegReg MEMSegReg1(
        .clk(CPU_CLK),
        .en(~StallM),
        .clear(FlushM),
        .AluOutE(AluOutE),
        .AluOutM(AluOutM), 
        .ForwardData2(ForwardData2),
        .StoreDataM(StoreDataM), 
        .RdE(RdE),
        .RdM(RdM),
        .PCE(PCE),
        .PCM(PCM),
        .RegWriteE(RegWriteE),
        .RegWriteM(RegWriteM),
        .MemToRegE(MemToRegE),
        .MemToRegM(MemToRegM),
        .MemWriteE(MemWriteE),
        .MemWriteM(MemWriteM),
        .LoadNpcE(LoadNpcE),
        .LoadNpcM(LoadNpcM)
    );

    // ---------------------------------------------
    // WB stage
    // ---------------------------------------------
    WBSegReg WBSegReg1(
        .clk(CPU_CLK),
        .en(~StallW),
        .clear(FlushW),
        .A(AluOutM),
        .WD(StoreDataM),
        .WE(MemWriteM),
        .RD(DM_RD),
        .LoadedBytesSelect(LoadedBytesSelect),
        .A2(CPU_Debug_DataRAM_A2),
        .WD2(CPU_Debug_DataRAM_WD2),
        .WE2(CPU_Debug_DataRAM_WE2),
        .RD2(CPU_Debug_DataRAM_RD2),
        .ResultM(ResultM),
        .ResultW(ResultW), 
        .RdM(RdM),
        .RdW(RdW),
        .RegWriteM(RegWriteM),
        .RegWriteW(RegWriteW),
        .MemToRegM(MemToRegM),
        .MemToRegW(MemToRegW)
    );
    
    DataExt DataExt1(
        .IN(DM_RD),
        .LoadedBytesSelect(LoadedBytesSelect),
        .RegWriteW(RegWriteW),
        .OUT(DM_RD_Ext)
    );
    // ---------------------------------------------
    // Harzard Unit
    // ---------------------------------------------
    HarzardUnit HarzardUnit1(
        .CpuRst(CPU_RST),
        .BranchE(BranchE),
		.BranchPredictedE(BranchPredictedE), //for BTB
		.BranchPredictedTakenE(BranchPredictedTakenE), //for BHT
        .JalrE(JalrE),
        .JalD(JalD),
        .Rs1D(Rs1D),
        .Rs2D(Rs2D),
        .Rs1E(Rs1E),
        .Rs2E(Rs2E),
        .RegReadE(RegReadE),
        .MemToRegE(MemToRegE),
        .RdE(RdE),
        .RdM(RdM),
        .RegWriteM(RegWriteM),
        .RdW(RdW),
        .RegWriteW(RegWriteW),
        .ICacheMiss(1'b0),
        .DCacheMiss(1'b0),
        .StallF(StallF),
        .FlushF(FlushF),
        .StallD(StallD),
        .FlushD(FlushD),
        .StallE(StallE),
        .FlushE(FlushE),
        .StallM(StallM),
        .FlushM(FlushM),
        .StallW(StallW),
        .FlushW(FlushW),
        .Forward1E(Forward1E),
        .Forward2E(Forward2E)
    	);    
    	         
endmodule
