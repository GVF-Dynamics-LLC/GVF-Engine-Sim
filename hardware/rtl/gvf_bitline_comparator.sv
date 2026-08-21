module gvf_bitline_comparator #(
    parameter WIDTH = 16,
    parameter EPSILON = 16'h000F
)(
    input  logic             clk,
    input  logic             rst_n,
    input  logic [WIDTH-1:0] signal_energy,
    input  logic [WIDTH-1:0] v_th_carrier,
    input  logic [WIDTH-1:0] entropy_val,
    input  logic [WIDTH-1:0] entropy_thresh,
    output logic             gated_clk_enable
);
    logic [WIDTH-1:0] diff;

    always_comb begin
        if (signal_energy > v_th_carrier)
            diff = signal_energy - v_th_carrier;
        else
            diff = v_th_carrier - signal_energy;

        if (entropy_val > entropy_thresh) begin
            gated_clk_enable = 1'b0;
        end else if (diff < EPSILON) begin
            gated_clk_enable = 1'b1;
        end else if (signal_energy >= v_th_carrier) begin
            gated_clk_enable = 1'b1;
        end else begin
            gated_clk_enable = 1'b0;
        end
    end
endmodule
