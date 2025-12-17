module elevator_tb;

    reg clk;
    reg reset;
    reg request_valid;
    reg [1:0] request_floor;

    wire [1:0] current_floor;
    wire moving;
    wire direction;

    elevator_controller dut (
        .clk(clk),
        .reset(reset),
        .request_valid(request_valid),
        .request_floor(request_floor),
        .current_floor(current_floor),
        .moving(moving),
        .direction(direction)
    );

    always #5 clk = ~clk;

    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, elevator_tb);

        clk = 0;
        reset = 1;
        request_valid = 0;
        request_floor = 0;

        #10 reset = 0;

        #10 request_floor = 2'd3;
            request_valid = 1;

        #40 request_valid = 0;

        #20 request_floor = 2'd1;
            request_valid = 1;

        #40 request_valid = 0;

        #50 $finish;
    end

endmodule
