module elevator_controller (
    input clk,
    input reset,
    input request_valid,
    input [1:0] request_floor,
    output reg [1:0] current_floor,
    output reg moving,
    output reg direction
);

    // direction: 1 = up, 0 = down

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            current_floor <= 2'd0;
            moving <= 1'b0;
            direction <= 1'b0;
        end else begin
            if (request_valid) begin
                if (current_floor < request_floor) begin
                    direction <= 1'b1;
                    moving <= 1'b1;
                    current_floor <= current_floor + 1'b1;
                end else if (current_floor > request_floor) begin
                    direction <= 1'b0;
                    moving <= 1'b1;
                    current_floor <= current_floor - 1'b1;
                end else begin
                    moving <= 1'b0;
                end
            end else begin
                moving <= 1'b0;
            end
        end
    end

endmodule
