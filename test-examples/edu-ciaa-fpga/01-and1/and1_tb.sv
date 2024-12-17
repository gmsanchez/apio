`default_nettype none
`define DUMPSTR(x) `"x.vcd`"
`timescale 100 ns / 10 ns

module and1_testbench();

    logic a, b, s;

    // Instantiate device under test
    and1 dut(a, b, s);

    // Apply inputs one at a time
    initial begin
        $dumpfile(`DUMPSTR(`VCD_OUTPUT));
        $dumpvars(0, and1_testbench);

        a = 0; b = 0;
        #10;
        a = 0; b = 1;
        #10;
        a = 1; b = 0;
        #10;
        a = 1; b = 1;
        #10;

        $display("End of simulation");
        $finish;

    end
endmodule