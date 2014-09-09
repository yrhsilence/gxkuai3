strategy = { num = 9, before = 40, after = 5}
bonus = {
    nil, nil, 240, 80, 40, 25, 16, 12, 10, 9, 9, 10, 12, 16, 25, 40, 80, 240
}

sum = 0
function get_win_number(str, sep)
    while true do
        local pos = string.find(str, sep);
        if not pos then
            return str;
        end
        str = string.sub(str, pos + 1);
    end 
end

function eami(index, flag)
   if (flag == -1) then
       return -1 * 2 * ((2 ^ index) - 1)
   else 
       return 2 ^ (index - 1)  * bonus[strategy['num']]
   end
end

function buy(index, win_nums)
    for i = 1, strategy['after'] do
        local pos = index + i;
        if win_nums[pos] == nil then
            return eami(i, -1)
        end
        if (win_nums[pos] == strategy['num']) then
            return eami(i, 1); 
        end 
    end
    return eami(strategy['after'], -1)
end

function calc(win_nums)
    local sum = 0
    local step = 0 
    for i = 0, #win_nums do
        if (win_nums[i] ~= strategy['num']) then
            step = step + 1;
            if (step == strategy['before']) then
                excu = buy(i, win_nums);
                print (i, win_nums[i], excu)
                sum = sum + excu
                --print('buy one: ', i, win_nums[i], excu);
            end
        else
            step = 0;
        end
    end
    return sum
end

function process(f_addr)
    local count = 0;
    local win_nums = {};
    local file = io.open(f_addr, "r");
    for line in file:lines() do
        win_nums[count] = tonumber(get_win_number(line, ":"));
        count = count + 1
    end
    file:close()

    res = calc(win_nums)    
    print("res: ", res)
end

function main()
    process("data/all")
end

main()
