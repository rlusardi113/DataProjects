#include<iostream>
#include<cstdlib>     
#include<ctime>       
#include<string>
#include<vector>
#include<algorithm>
#include <random>

using namespace std;

//organismjump
class Organism {
    private:
        int position;
        int lifespan;
        char symbol;
        bool hasMoved;
    public:
        //constructors
        Organism(): position(0), lifespan(0), symbol('-'), hasMoved(false){};
        Organism(int positionInput): position(positionInput), lifespan(0), symbol('-'), hasMoved(false){};
        Organism(int positionInput, int lifespanInput, char symbolInput, bool hasMovedInput): position(positionInput), lifespan(lifespanInput), symbol(symbolInput), hasMoved(hasMovedInput){};

        //getters
        int get_position() {return position;}
        int get_lifespan() {return lifespan;}
        char get_symbol() {return symbol;}
        bool get_hasMoved() {return hasMoved;}
        
        //setters
        void set_position(int positionInput){position = positionInput;}
        void set_hasMoved(bool hasMovedInput);
        void reset_lifespan(){lifespan = 0;}
        void set_lifespan(int lifespanInput){lifespan = lifespanInput;}
        void update_lifespan(){lifespan+=1;}

        //breed function works the same logically regardless of whether it is ant or doodlebug, so have just defined in organism
        void breed(int breedTime, Organism* orgArr[]);

        //have also defined starve in organism, but made logic only apply to doodlebugs for now (since all organisms can starve)
        void starve(int starveTime, Organism* orgArr[]);

        //move and starve functions, which will be defined separately for each of Ant and Doodlebug (virtual)
        virtual void move(int direction, Organism* orgArr[]);
        virtual void update_daysSinceLastFeed(){/*intentionally empty. defined for doodlebug. not necessary for ants or organisms*/};
        virtual void reset_daysSinceLastFeed(){/*intentionally empty. defined for doodlebug. not necessary for ants or organisms*/}
        virtual int get_daysSinceLastFeed(){return 0;/*intentionally empty. defined for doodlebug. not necessary for ants or organisms*/};

};

//antjump
class Ant : public Organism {
    public:
        Ant(int positionInput, int lifespanInput, bool hasMovedInput) : Organism(positionInput, lifespanInput, 'x', hasMovedInput){};
        virtual void move(int direction, Organism* orgArr[]);
};

//doodlebugjump
class Doodlebug : public Organism {
    public:
        int daysSinceLastFeed;
        Doodlebug(int positionInput, int lifespanInput, bool hasMovedInput, int daysSinceLastFeedInput) : Organism(positionInput, lifespanInput, 'O', hasMovedInput){daysSinceLastFeed = daysSinceLastFeedInput;};

        //getters
        int get_daysSinceLastFeed(){return daysSinceLastFeed;};

        //setters
        void update_daysSinceLastFeed(){daysSinceLastFeed++;}
        void reset_daysSinceLastFeed(){daysSinceLastFeed = 0;}

        //other functions
        virtual void move(int direction, Organism* orgArr[]);
        //starve function
};

//mainjump
int main()
{
    //build world of 400 elements. Doodlebugs and Ants are Derived Classes of Organism Base Class
    int worldSize = 400;
    Organism** world = new Organism*[worldSize];

    //code to initialize world
    const int initialAntCount = 100, initialDoodleBugCount = 5;
    const int antBreedTime = 3;
    const int doodlebugBreedTime = 8, doodlebugStarveTime = 3;
    vector<int> initialPositionVector;
    for (int i = 0; i < worldSize; i++){
        world[i] = new Organism(i+1);
    }

    //loop to initialize and populate vector. elements in Vector will then be randomized (to determine random starting positions for ants and doodlebugs) 
    for (int i = 1; i <= worldSize; i++){
        initialPositionVector.push_back(i);
    }
    srand(time(0));
    auto rng = std::default_random_engine {};
    shuffle(initialPositionVector.begin(), initialPositionVector.end(), rng);

    //populate the ants and doodlebugs at random points in the array
    for (int i = 0; i < initialAntCount + initialDoodleBugCount; i++){
        delete world[initialPositionVector[i] - 1];
        if (i < initialAntCount){
            world[initialPositionVector[i]- 1] = new Ant(initialPositionVector[i], 0, false);
        }
        else {
            world[initialPositionVector[i] - 1] = new Doodlebug(initialPositionVector[i], 0, false, 0);
        }
    }

    //main section of code for simulation of world
    bool flag = true;
    bool areThereAntsorDoodlebugs = true;
    string userInput;
    int time = 0;

    cout<<"Press enter to begin simulation"<<endl;
    while (flag && areThereAntsorDoodlebugs){
        getline(cin, userInput);
        if (!userInput.empty()){
            flag = false;
            break;
        }
        else {
            //print the world at time i
            cout<<"World at time "<<time<<endl;
            for (int i = 0; i < worldSize; i++){
                if ((i+1) % 20 == 0){
                    cout<<world[i]->get_symbol()<<endl;
                }
                else {
                    cout<<world[i]->get_symbol();
                }
            }
            
            //move the ants
            for (int i = 0; i < worldSize; i++){
                if (world[i]->get_symbol() == 'x'){
                    int randomDirection = (rand()%4)+1;//generate number 1-4 (N,S,E,W) which indicates direction
                    world[i]->move(randomDirection, world);
                }
            }

            //move the doodlebugs
            for (int i = 0; i < worldSize; i++){
                if (world[i]->get_symbol() == 'O'){
                    int randomDirection = (rand()%4)+1;
                    world[i]->move(randomDirection, world);
                }
            }
            
            // breed the doodlebugs
            for (int i = 0; i < worldSize; i++){
                if (world[i]->get_symbol() == 'O'){
                    world[i]->breed(doodlebugBreedTime, world);
                }
            }

            //breed the ants
            for (int i = 0; i < worldSize; i++){
                if (world[i]->get_symbol() == 'x'){
                    world[i]->breed(antBreedTime, world);
                }
            }

            //starve doodlebugs
            for (int i = 0; i < worldSize; i++){
                if (world[i]->get_symbol() == 'O'){
                    world[i]->starve(doodlebugStarveTime, world);
                }
            }

            //reset the hasMoved tracker for the next turn and update lifespan for all ants and doodlebugs
            //update days since last feed for doodlebugs
            for (int i = 0; i < worldSize; i++){
                world[i]->set_hasMoved(false);
                world[i]->update_lifespan();
                if (world[i]->get_symbol() == 'O'){
                    world[i]->update_daysSinceLastFeed();
                }
            }

            //check if there are any ants or doodlebugs left in the world
            int antsLeftCount = 0, doodlebugsLeftCount = 0;
            for (int i = 0; i < worldSize; i++){
                if (world[i]->get_symbol() == 'O'){
                    doodlebugsLeftCount++;
                }
                else if (world[i]->get_symbol() == 'x'){
                    antsLeftCount++;
                }
            }

            if (doodlebugsLeftCount == 0 || antsLeftCount == 0){
                areThereAntsorDoodlebugs = false;
            }

            time++;
            cout<<"Press enter to continue. Otherwise enter anything to exit"<<endl;
        }
    }

    //goodbye world
    cout<<"End of simulation"<<endl;
    for (int i = 0; i <worldSize; i++){
        delete world[i];
    }
    delete[] world;

    return 0;
}

void Organism::move(int direction, Organism* orgArr[]){
    int currentPosition = (this -> get_position());
    bool hasMoved = (this -> get_hasMoved());
    char thisSymbol = (this -> get_symbol());

    //if this has not yet moved, and it is an ant or doodlebug
    if (!hasMoved && (thisSymbol == 'x' || thisSymbol == 'O')){
        if (direction == 1 && currentPosition > 20){//N. Want to exclude ants moving in top row (similar logic for S,E,W)
            this->set_position(currentPosition-20);
        }

        else if (direction == 2 && currentPosition < 381){//S
            this->set_position(currentPosition+20);
        }

        else if (direction == 3 && currentPosition % 20 != 0){//E
            this->set_position(currentPosition+1);
        }

        else if (direction == 4 && currentPosition % 20 != 1){//W
            this->set_position(currentPosition-1);
        }
    }
    return;
}

void Organism::breed(int breedTime, Organism* orgArr[]){
    int currentPosition = this->get_position();
    int lifespan = this->get_lifespan();
    char symbol = this->get_symbol();
    int parentPosition = this->get_position();
    int lastFeedTime = this->get_daysSinceLastFeed();
    int childPosition;
    bool breedFlag = false;

    if (lifespan > 0 && lifespan % breedTime == 0 && (symbol == 'x' || symbol == 'O')){  
        for (int direction = 1; direction <= 4; direction++){//check N, then S, E, W to see if vacant
            //logic is generally the same for all for directions
            //if there is an empty space in the ith direction, then breed a new ant or doodlebug as appropriate
            //note, Doodlebug daysSinceLastFeed set to -1 given logic of main loop to increment daysSinceLastFeed after breeding
            if (direction == 1 && parentPosition > 20){
                childPosition = parentPosition - 20;
                if (orgArr[childPosition-1]->get_symbol() == '-'){
                    delete orgArr[childPosition-1];
                    if (symbol == 'x'){
                        orgArr[childPosition-1] = new Ant(childPosition, -1, true);
                        break;
                    }
                    else if (symbol == 'O'){
                        orgArr[childPosition-1] = new Doodlebug(childPosition, -1, true, -1);
                        break;
                    }
                }
            }
            
            else if (direction == 2 && parentPosition < 381){
                childPosition = parentPosition + 20;
                if (orgArr[childPosition-1]->get_symbol() == '-'){
                    delete orgArr[childPosition-1];
                    if (symbol == 'x'){
                        orgArr[childPosition-1] = new Ant(childPosition, -1, true);
                        break;
                    }
                    else if (symbol == 'O'){
                        orgArr[childPosition-1] = new Doodlebug(childPosition, -1, true, -1);
                        break;
                    }
                }
            }

            else if (direction == 3 && parentPosition % 20 != 0){
                childPosition = parentPosition + 1;
                if (orgArr[childPosition-1]->get_symbol() == '-'){
                    delete orgArr[childPosition-1];
                    if (symbol == 'x'){
                        orgArr[childPosition-1] = new Ant(childPosition, -1, true);
                        break;
                    }
                    else if (symbol == 'O'){
                        orgArr[childPosition-1] = new Doodlebug(childPosition, -1, true, -1);
                        break;
                    }
                }
            }
            
            else if (direction == 4 && parentPosition % 20 != 1){
                childPosition = parentPosition - 1;
                if (orgArr[childPosition-1]->get_symbol() == '-'){
                    delete orgArr[childPosition-1];
                    if (symbol == 'x'){
                        orgArr[childPosition-1] = new Ant(childPosition, -1, true);
                        break;
                    }
                    else if (symbol == 'O'){
                        orgArr[childPosition-1] = new Doodlebug(childPosition, -1, true, -1);
                        break;
                    }
                }
            }
        }
    }
        
    return;
}

void Organism::starve(int starveTime, Organism* orgArr[]){
    char symbol = this->get_symbol();
    int daysSinceLastFeed = this->get_daysSinceLastFeed();
    int position = this->get_position();

    if (symbol == 'O' && daysSinceLastFeed == starveTime){
        delete orgArr[position-1];
        orgArr[position-1] = new Organism();
    }
    
    return;
}

void Organism::set_hasMoved(bool hasMovedInput){
    if (this->get_symbol() == 'x' || this->get_symbol() == 'O'){
        this->hasMoved = hasMovedInput;
    }
    
    return;
}

void Ant::move(int direction, Organism* orgArr[]){
    int oldPosition = (this -> get_position());
    int currentLifespan = (this -> get_lifespan());

    //this call to move will update the position of the ant to the new position, regardless of whether the cell is empty or not
    //else statement below will be adjusted position of ant back to original position if move is not a valid move
    Organism::move(direction, orgArr);
    int newPosition = (this -> get_position());

    //if the space the ant is trying to move to is empty (denoted by '-' char), and the move is eligible (e.g. it is not trying to move up from the top row)
    //then move the ant to the position in the array (via creating a new ant) and then replace the location where the ant was with an empty organism
    if (orgArr[newPosition-1]->get_symbol() == '-' && oldPosition != newPosition){
        delete orgArr[newPosition-1];
        orgArr[newPosition-1] = new Ant(newPosition, currentLifespan, true);

        delete orgArr[oldPosition-1];
        orgArr[oldPosition-1] = new Organism(oldPosition);
    }

    else {//don't move the ant
        this -> set_position(oldPosition);
    }

    return;
}

void Doodlebug::move(int direction, Organism* orgArr[]){
    int oldPosition = (this -> get_position());
    int currentLifespan = (this -> get_lifespan());
    int currentDaysSinceLastFeed = (this -> get_daysSinceLastFeed());

    Organism::move(direction, orgArr);
    int newPosition = (this -> get_position());

    //if the space the doodlebug is trying to move to is empty or is an ant, and the move is eligible (e.g. it is not trying to move up from the top row)
    if ((orgArr[newPosition-1]->get_symbol() == '-' || orgArr[newPosition-1]->get_symbol() == 'x') && oldPosition != newPosition){
        if (orgArr[newPosition-1]->get_symbol() == 'x'){
            delete orgArr[newPosition-1];
            orgArr[newPosition-1] = new Doodlebug(newPosition, currentLifespan, true, -1);
        }
        else if (orgArr[newPosition-1]->get_symbol() == '-'){
            delete orgArr[newPosition-1];
            orgArr[newPosition-1] = new Doodlebug(newPosition, currentLifespan, true, currentDaysSinceLastFeed);
        }

        delete orgArr[oldPosition-1];
        orgArr[oldPosition-1] = new Organism(oldPosition);
    }

    else {
        this -> set_position(oldPosition);
    }

    return;
}