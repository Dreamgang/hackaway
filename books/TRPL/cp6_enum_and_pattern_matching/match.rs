#[derive(Debug)]
enum UsState {
    Alabama,
    Alaska,
    So,
    And,
    Soon,
    Etc,
    Haha,
}

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState), // bind value here
}


fn value_in_cents(coin: Coin) -> i32 {
    match coin {
        Coin::Penny => {
            println!("Lucky Penny!");
            1
        },
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {:?}!", state);
            25
        },
    }
}

fn main() {
    let coin = Coin::Penny;
    let v = value_in_cents(coin);
    println!("{}", v);

    let coin  = Coin::Quarter(UsState::Haha);
    let v = value_in_cents(coin);
    println!("{}", v);

}